from django.urls import path
from reports import views

app_name = 'reports'
urlpatterns = [
    # レポート
    path('list/', views.get_report, name='list'),   # 一覧
]