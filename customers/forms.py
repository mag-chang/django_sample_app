from django.forms import ModelForm
from customers.models import Customer


class CustomerForm(ModelForm):
    """
    顧客フォーム
    """
    class Meta:
        model = Customer
        fields = (
            'name',
            'gender',
            'age',
        )