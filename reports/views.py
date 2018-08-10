from datetime import date
from dateutil.relativedelta import relativedelta
from django.shortcuts import render
from reports.forms import ReportsChoiceYearMonthForm
from lessons.models import Plan, History
from customers.models import Customer


class GenderPriceList(object):
    def __init__(self):
        self.plan = ''
        self.gender = ''
        self.age_range = 0  # optional
        self.lesson_count = 0
        self.customer_count = 0
        self.price = ''


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
    end_date = start_date + relativedelta(months=1) - relativedelta(days=1)

    return_list = []

    # 全ジャンルを取得
    all_plans = Plan.objects.all().order_by('id')

    for plan in all_plans:
        gender_count_dict = {}
        for gender_tuple in Customer.GENDER:
            gender_count_dict[gender_tuple[0]] = []

        histories = History.objects.filter(
            lesson_plan=plan,
            lesson_on__gte=start_date,
            lesson_on__lte=end_date,
        )

        if histories:

                # ex. こんなListが受講ジャンル毎に作られる
                #  [
                #    { '男性':
                #       [
                #           {
                #                'customer_id': 1
                #                'hour': 5
                #           },
                #           {
                #                'customer_id': 1
                #                'hour': 12
                #           },
                #           {
                #                'customer_id': 2
                #                'hour': 3
                #           },
                #       ]
                #    },
                #    { '女性':
                #        [
                #           {
                #                'customer_id': 3
                #                'hour': 10
                #           },
                #           {
                #                'customer_id': 4
                #                'hour': 3
                #           },
                #        ]
                #    }
                #  ]

            for history in histories:
                gender_count_dict[history.customer.gender].append({'customer_id':history.customer.id, 'hour': history.lesson_hour})

        for key, value in gender_count_dict.items():
            gender_price_list = GenderPriceList()
            gender_price_list.plan = plan.name

            gender_price_list.gender = key
            gender_price_list.lesson_count = len(value)
            l = []
            sum_hours = 0
            for v in value:
                l.append(v['customer_id'])
                sum_hours += v['hour']
            gender_price_list.customer_count = len(sorted(set(l), key=l.index))
            gender_price_list.price = plan.calculate_price(sum_hours)

            return_list.append(gender_price_list)

    # フォームの初期値に選択済みの値をセット
    form = ReportsChoiceYearMonthForm({'select_year_month':selected_year_month})

    return render(
        request,
        'reports/list.html',
        {
            'form': form,
            'genre_and_gender_list': return_list,
        },
    )
