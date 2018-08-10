from django.forms import ModelForm, DateField, SelectDateWidget
from lessons.models import History, Genre, CalculateLogic


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
            'lesson_genre',
            'lesson_on',
            'lesson_hour',
        )

class GenreForm(ModelForm):
    """
    受講ジャンルフォーム
    """
    class Meta:
        model = Genre
        fields = (
            'name',
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