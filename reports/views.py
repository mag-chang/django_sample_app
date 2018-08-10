from datetime import date
from dateutil.relativedelta import relativedelta
from django.shortcuts import render
from reports.forms import ReportsChoiceYearMonthForm
from lessons.models import Genre, History
from customers.models import Customer
import pandas as pd


class GenreGenderAgeRange(object):
    """
    受講ジャンル、年齢などを保持してtemplateに返すためのオブジェクト
    """
    def __init__(self):
        self.genre = ''
        self.gender = ''
        self.age_range = 0
        self.lesson_count = 0
        self.customer_count = 0
        self.price = 0


def get_report(request, year=None, month=None):
    """
    請求一覧を取得する
    """

    # 日付選択プルダウンからのリクエスト
    selected_year_month = None
    if request.POST:
        selected_year_month = request.POST.get('select_year_month')
        split_year_month = selected_year_month.split('/')
        year = int(split_year_month[0])
        month = int(split_year_month[1])
    else:
        if not year or not month:
            today = date.today()
            year = today.year
            month = today.month

    start_date = date(year, month, 1)
    end_date = start_date + relativedelta(months=1) - relativedelta(days=1) # 翌月1日の前日を取得

    genre_and_gender_list = []
    genre_and_age_range_list = []

    # 全ジャンルを取得
    all_genres = Genre.objects.all().order_by('id')

    # ジャンル毎に集計
    for genre in all_genres:
        gender_count_dict = {}
        # 最初に性別をキーにしたdictを作成
        for gender_tuple in Customer.GENDER:
            gender_count_dict[gender_tuple[0]] = []

        histories = History.objects.filter(
            lesson_genre=genre,
            lesson_on__gte=start_date,
            lesson_on__lte=end_date,
        )

        if histories:
            # 受講履歴があれば受講履歴毎の集計用データを作成
            for history in histories:
                gender_count_dict[history.customer.gender].append(
                    {
                        'customer_id': history.customer.id,
                        'hour': history.lesson_hour,
                        'age_range': int((history.customer.age / 10)) * 10,
                    }
                )
                # ex. gender_count_dictは、こんなdictが受講ジャンル毎に作られる
                #    { '男性':
                #       [
                #           {
                #                'customer_id': 1,
                #                'hour': 5,
                #                'age_range': 10,
                #           },
                #           {
                #                'customer_id': 1,
                #                'hour': 12,
                #                'age_range': 10,
                #           },
                #           {
                #                'customer_id': 2,
                #                'hour': 3,
                #                'age_range': 30,
                #           },
                #       ]
                #    },
                #    { '女性':
                #        [
                #           {
                #                'customer_id': 3,
                #                'hour': 10,
                #                'age_range': 20,
                #           },
                #           {
                #                'customer_id': 4,
                #                'hour': 3,
                #                'age_range': 30,
                #           },
                #        ]
                #    }

        # 性別毎のdictをループ
        for key, value in gender_count_dict.items():
            df = pd.DataFrame(value)

            # ジャンルと性別別向けのList作成
            gender_price_list = GenreGenderAgeRange()
            gender_price_list.genre = genre.name

            gender_price_list.gender = key
            gender_price_list.lesson_count = len(value)

            if len(df):
                sum_hours_df = df.groupby('customer_id')['hour'].sum()
                gender_price_list.customer_count = len(sum_hours_df)
                sub_total_price = 0
                for i in sum_hours_df.__iter__():
                    sub_total_price += genre.calculate_price(i)
                gender_price_list.price = sub_total_price

            genre_and_gender_list.append(gender_price_list)

            # ジャンルと年齢層別向けのList作成
            for age_range in range(10, 71, 10):
                genre_and_age_range = GenreGenderAgeRange()
                genre_and_age_range.genre = genre.name
                genre_and_age_range.gender = key
                genre_and_age_range.age_range = age_range

                if len(df):
                    target_age_range_df = df[df['age_range'] == age_range]
                    genre_and_age_range.lesson_count = len(target_age_range_df)
                    genre_and_age_range.customer_count = len(target_age_range_df['customer_id'].unique())
                    genre_and_age_range.price = genre.calculate_price(target_age_range_df['hour'].sum())

                genre_and_age_range_list.append(genre_and_age_range)

    # フォームの初期値に選択済みの値をセット
    form = ReportsChoiceYearMonthForm({'select_year_month':selected_year_month})

    return render(
        request,
        'reports/list.html',
        {
            'form': form,
            'genre_and_gender_list': genre_and_gender_list,
            'genre_and_age_range_list': genre_and_age_range_list,
        },
    )
