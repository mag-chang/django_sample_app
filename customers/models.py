from django.db import models


class Customer(models.Model):
    """
    顧客
    """
    MALE = 'M'
    FEMALE = 'F'
    GENDER = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )

    name = models.CharField(
        max_length=30,
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER,
    )
    age = models.SmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
