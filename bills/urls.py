from django.urls import path
from bills import views

app_name = 'bills'
urlpatterns = [
    # 請求一覧
    path('list/', views.get_bill_list, name='list'),   # 一覧
]