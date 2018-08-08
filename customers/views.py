from django.shortcuts import render
from django.http import HttpResponse

from customers.models import Customer

def get_customer_list(request):
    """
    顧客一覧を取得する
    :param request:
    :return:
    """

    customers = Customer.objects.all().order_by('id')
    # return render(request,
    #               'customers/list.html',
    #               {'customers': customers},
    #               )
    return render(request,
                  'customers/list.html',
                  {'customers': '田中太郎'},
                  )
