from django.db import models
from customers.models import Customer


class Plan(models.Model):
    """
    受講プラン
    """
    name = models.CharField(
        max_length=30,
    )
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField(null=True)
    calculate_logic_name = models.CharField(
        max_length=30,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class History(models.Model):
    """
    受講記録
    """
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    lesson_at = models.DateTimeField()
    lesson_plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    lesson_hour = models.IntegerField()
    lesson_fee = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
