from django.urls import path
from customers import views

app_name = 'customers'
urlpatterns = [
    # 顧客
    path('list/', views.get_customer_list, name='list'),   # 一覧
    path('add/', views.customer_edit, name='add'),  # 登録
    path('edit/<int:customer_id>/', views.customer_edit, name='edit'),  # 修正
]