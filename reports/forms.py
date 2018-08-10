from datetime import date
from dateutil.relativedelta import relativedelta
from django.forms import Form, ChoiceField, Select
from bills.forms import ChoiceYearMonthForm


class ReportsChoiceYearMonthForm(ChoiceYearMonthForm):
    """
    年月選択フォーム
    """
    display_format = '%Y年%m月'
    key_format = '%Y/%m'

    today = date.today()

    current_year_month = today
    previous_year_month = today - relativedelta(months=1)
    pre_previous_year_month = today - relativedelta(months=2)

    choice_month = (
        (current_year_month.strftime(key_format), current_year_month.strftime(display_format)),
        (previous_year_month.strftime(key_format), previous_year_month.strftime(display_format)),
        (pre_previous_year_month.strftime(key_format), pre_previous_year_month.strftime(display_format)),
    )

    select_year_month = ChoiceField(
        label='対象月',
        widget=Select(),
        choices=choice_month,
    )
