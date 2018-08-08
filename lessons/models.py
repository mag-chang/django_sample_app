from django.db import models
from customers.models import Customer


class Plan(models.Model):
    """
    受講プラン
    """
    name = models.CharField(
        max_length=30,
    )
    avail_datetime_start = models.DateTimeField()
    avail_datetime_end = models.DateTimeField(null=True)
    calculate_charge_logic = models.CharField(
        max_length=30,
    )


class History(models.Model):
    """
    受講記録
    """
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    lesson_plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    lesson_hour = models.IntegerField()
    lesson_fee = models.IntegerField()
