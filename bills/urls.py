from django.urls import path
from bills import views

app_name = 'bills'
urlpatterns = [
    # 請求一覧
    path('list/<int:year>/<int:month>/', views.get_bill_list, name='list_with_year_month'),   # 一覧
    path('list/', views.get_bill_list, name='list'),   # 一覧
]