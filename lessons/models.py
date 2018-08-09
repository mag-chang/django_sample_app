from django.db import models
from customers.models import Customer
from lessons.calculate_logics import *

# class CalculateLogic(models.Model):
#     """
#     料金計算ロジック
#     """
#     name = models.CharField(
#         max_length=30,
#     )
#     # 料金計算ロジックの関数名を指定する
#     logic_name = models.CharField(
#         max_length=30,
#     )
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#
# class Plan(models.Model):
#     """
#     受講プラン
#     """
#     name = models.CharField(
#         max_length=30,
#     )
#     started_month = models.PositiveSmallIntegerField()
#     ended_month = models.PositiveSmallIntegerField(null=True)
#     calculate_logic = models.ForeignKey(CalculateLogic, on_delete=models.PROTECT)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#
# class History(models.Model):
#     """
#     受講記録
#     """
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     lesson_on = models.DateField()
#     lesson_plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
#     lesson_hour = models.IntegerField()
#     # lesson_price = models.IntegerField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
