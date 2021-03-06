from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from customers.models import Customer
from customers.forms import CustomerForm


def get_customer_list(request):
    """
    顧客一覧を取得する
    """

    customers = Customer.objects.all().order_by('id')
    return render(request,
                  'customers/list.html',
                  {'customers': customers},
                  )

def customer_edit(request, customer_id=None):
    """
    顧客を新規作成/編集する
    """

    if customer_id:
        customer = get_object_or_404(Customer, pk=customer_id)
    else:
        customer = Customer()

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.save()
            return redirect('customers:list')
    else:
        form = CustomerForm(instance=customer)

    return render(
        request,
        'customers/edit.html',
        dict(form=form, customer_id=customer_id)
    )
