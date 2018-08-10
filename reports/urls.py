from django.urls import path
from reports import views

app_name = 'reports'
urlpatterns = [
    # レポート
    # path('list/<int:year>/<int:month>/', views.get_bill_list, name='list_with_year_month'),   # 一覧
    path('list/', views.get_report, name='list'),   # 一覧
]