from dateutil.relativedelta import relativedelta
from datetime import date

from django.shortcuts import render
from lessons.models import History
from customers.models import Customer
from bills.forms import ChoiceYearMonthForm

class SumLessonHistory(object):
    def __init__(self):
        self.customer_id = 0
        self.customer_name = ''
        self.lesson_name_sum = ''
        self.lesson_name_count = 0
        self.lesson_total_count = 0
        self.lesson_total_price = 0


def get_bill_list(request, year=None, month=None):
    """
    請求一覧を取得する
    """

    # 全顧客を取得
    all_customers = Customer.objects.all().order_by('id')

    today = date.today()
    if not year or not month:
        year = today.year
        month = today.month

    start_date = date(year, month, 1)
    end_date = start_date + relativedelta(months=1) - relativedelta(days=1)

    # SumLessonHistoryのList(templateに返却)
    sum_histories = []

    for customer in all_customers:
        # 顧客毎の受講履歴を取得
        lesson_history = History.objects.filter(
            customer=customer,
            lesson_on__gte=start_date,
            lesson_on__lte=end_date,
        ).order_by(
            'lesson_plan',
        )

        sum_lesson_history = SumLessonHistory()
        sum_lesson_history.customer_id = customer.id
        sum_lesson_history.customer_name = customer.name

        # 受講履歴があれば内容を集計
        if lesson_history:
            before_plan = None
            lesson_name_list = []
            subtotal_hour_per_lesson = 0
            subtotal_price = 0

            # 受講履歴があれば内容を集計
            for history in lesson_history:
                # レッスン内容が変わったら累計時間から料金計算
                if before_plan and history.lesson_plan.id != before_plan.id:
                    subtotal_price += before_plan.calculate_price(subtotal_hour_per_lesson)
                    subtotal_hour_per_lesson = 0

                lesson_name_list.append(history.lesson_plan.name)
                subtotal_hour_per_lesson += history.lesson_hour
                before_plan = history.lesson_plan

            else:
                # forの最後も料金計算
                subtotal_price += before_plan.calculate_price(subtotal_hour_per_lesson)

            # レッスンの合計回数
            sum_lesson_history.lesson_total_count = len(lesson_name_list)

            # レッスンのユニーク名とその回数
            unique_lesson_name_list = sorted(set(lesson_name_list), key=lesson_name_list.index)
            sum_lesson_history.lesson_name_sum = '/'.join(unique_lesson_name_list)
            sum_lesson_history.lesson_name_count = len(unique_lesson_name_list)

            # 全レッスン合計金額
            sum_lesson_history.lesson_total_price = subtotal_price

        sum_histories.append(sum_lesson_history)

    #
    #
    #
    #
    #
    #
    #
    #
    # for idx, history in enumerate(histories):
    #     if before_customer_id and history.customer.id != before_customer_id:
    #         print('顧客変わったよ！')
    #         sum_lesson_history = SumLessonHistory()
    #         sum_lesson_history.customer_id = before_customer_id
    #         sum_lesson_history.customer_name = before_customer_name
    #         sum_lesson_history.lesson_total_count = len(lesson_name_list)
    #
    #         unique_lesson_name_list = sorted(set(lesson_name_list), key=lesson_name_list.index)
    #         sum_lesson_history.lesson_name_sum = '/'.join(unique_lesson_name_list)
    #         sum_lesson_history.lesson_name_count = len(unique_lesson_name_list)
    #
    #         sum_lesson_history.lesson_total_price = subtotal_price
    #
    #         sum_histories.append(sum_lesson_history)
    #         print(sum_lesson_history)
    #
    #         subtotal_hour_per_lesson = 0
    #         subtotal_price = 0
    #         before_lesson_id = 0
    #     else:
    #         print('顧客変わってないよ！')
    #         if before_lesson_id and history.lesson_plan.id != before_lesson_id:
    #             print('ジャンル変わったよ！')
    #             subtotal_price += history.lesson_plan.calculate_price(subtotal_hour_per_lesson)
    #             subtotal_hour_per_lesson = 0
    #
    #         lesson_name_list.append(history.lesson_plan.name)
    #         subtotal_hour_per_lesson += history.lesson_hour
    #         print(subtotal_hour_per_lesson)
    #         print(history.lesson_plan.name)
    #         print(subtotal_price)
    #         before_lesson_id = history.lesson_plan.id
    #
    #     before_customer_id = history.customer.id
    #     before_customer_name = history.customer.name
    #
    #     if idx == len(histories) - 1:
    #         print('最後だよ！')
    #         sum_lesson_history = SumLessonHistory()
    #         sum_lesson_history.customer_id = before_customer_id
    #         sum_lesson_history.customer_name = before_customer_name
    #         sum_lesson_history.lesson_total_count = len(lesson_name_list)
    #
    #         unique_lesson_name_list = sorted(set(lesson_name_list), key=lesson_name_list.index)
    #         sum_lesson_history.lesson_name_sum = '/'.join(unique_lesson_name_list)
    #         sum_lesson_history.lesson_name_count = len(unique_lesson_name_list)
    #
    #         sum_lesson_history.lesson_total_price = subtotal_price
    #
    #         sum_histories.append(sum_lesson_history)

    form = ChoiceYearMonthForm(request.GET or None)
    return render(
        request,
        'bills/list.html',
        {
            'form': form,
            'billing_histories': sum_histories,
        },
    )
