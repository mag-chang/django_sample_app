from django.urls import path
from customers import views

app_name = 'customers'
urlpatterns = [
    # 顧客
    path('list/', views.get_customer_list),   # 一覧
]