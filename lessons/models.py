from django.utils import timezone
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from customers.models import Customer
from lessons.calculate_logics.logics import Logics


class CalculateLogic(models.Model):
    """
    料金計算ロジック
    """
    name = models.CharField(
        verbose_name='計算名称',
        max_length=30,
        unique=True,
    )
    # 料金計算ロジックの関数名を指定する
    logic_name = models.CharField(
        verbose_name='ロジック名称',
        help_text='(入力する値は担当者に要確認)',
        max_length=30,
        unique=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name

    def get_calculate_function(self):
        """
        自分自身の `logic_name` に対応した計算ロジックfunctionを返却する
        :return: function
        """
        return Logics().__getattribute__(str(self.logic_name))

class Genre(models.Model):
    """
    受講ジャンル
    """
    name = models.CharField(
        verbose_name='ジャンル名',
        max_length=30,
    )
    calculate_logic = models.ForeignKey(
        CalculateLogic,
        verbose_name='計算方法',
        on_delete=models.PROTECT,
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name

    def calculate_price(self, hour):
        """
        自分自身に設定されている `calculate_logic` でhourの料金を計算した結果を返却する
        :param hour: 料金計算する時間
        :return: 計算結果
        """
        calculate_function = self.calculate_logic.get_calculate_function()
        return calculate_function(hour)

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
        default=timezone.now().date(),
    )
    lesson_genre = models.ForeignKey(
        Genre,
        verbose_name='ジャンル',
        on_delete=models.CASCADE,
    )
    lesson_hour = models.PositiveSmallIntegerField(
        verbose_name='受講時間(h)',
        validators=[MinValueValidator(1), MaxValueValidator(12)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
