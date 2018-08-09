from django.forms import ModelForm, ModelChoiceField, DateField, SelectDateWidget
from lessons.models import History, Plan, CalculateLogic


class HistoryForm(ModelForm):
    """
    受講記録フォーム
    """
    lesson_on = DateField(
        label='受講日',
        widget=SelectDateWidget,
    )

    class Meta:
        model = History
        fields = (
            'customer',
            'lesson_plan',
            'lesson_on',
            'lesson_hour',
        )

class PlanForm(ModelForm):
    """
    受講ジャンルフォーム
    """
    started_on = DateField(
        label='適用開始年月日',
        widget=SelectDateWidget,
    )
    ended_on = DateField(
        label='適用終了年月日(省略可)',
        widget=SelectDateWidget,
        required=False,
    )

    class Meta:
        model = Plan
        fields = (
            'name',
            'started_on',
            'ended_on',
            'calculate_logic',
        )

class CalculateLogicForm(ModelForm):
    """
    料金計算ロジックフォーム
    """
    class Meta:
        model = CalculateLogic
        fields = (
            'name',
            'logic_name',
        )