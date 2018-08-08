from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Customer(models.Model):
    """
    顧客
    """
    MALE_STRING = '男性'
    FEMALE_STRING = '女性'
    GENDER = (
        (MALE_STRING, MALE_STRING),
        (FEMALE_STRING, FEMALE_STRING),
    )

    name = models.CharField(
        verbose_name='名前',
        max_length=30,
    )
    gender = models.CharField(
        verbose_name='性別',
        max_length=10,
        choices=GENDER,
    )
    age = models.PositiveSmallIntegerField(
        verbose_name='年齢',
        validators=[MinValueValidator(0), MaxValueValidator(150),])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
