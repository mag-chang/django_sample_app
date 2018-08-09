from django.db import models
from customers.models import Customer
from django.core.validators import MinValueValidator, MaxValueValidator


class CalculateLogic(models.Model):
    """
    料金計算ロジック
    """
    name = models.CharField(
        verbose_name='計算名称',
        max_length=30,
    )
    # 料金計算ロジックの関数名を指定する
    logic_name = models.CharField(
        verbose_name='ロジック名称',
        help_text='(入力する値は担当者に要確認)',
        max_length=30,
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name

class Plan(models.Model):
    """
    受講プラン
    """
    name = models.CharField(
        verbose_name='ジャンル名',
        max_length=30,
    )
    started_on = models.DateField(
        verbose_name='適用開始年月日',
    )
    ended_on = models.DateField(
        verbose_name='適用終了年月日(任意)',
        null=True,
    )
    calculate_logic = models.ForeignKey(
        CalculateLogic,
        verbose_name='計算方法',
        on_delete=models.PROTECT,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class History(models.Model):
    """
    受講記録
    """
    customer = models.ForeignKey(
        Customer,
        verbose_name='顧客名',
        on_delete=models.CASCADE,
    )
    lesson_on = models.DateField(
        verbose_name='受講日',
    )
    lesson_plan = models.ForeignKey(
        Plan,
        verbose_name='ジャンル',
        on_delete=models.CASCADE,
    )
    lesson_hour = models.PositiveSmallIntegerField(
        verbose_name='受講時間(h)',
        validators=[MinValueValidator(1), MaxValueValidator(12)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
