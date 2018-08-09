from django.urls import path
from lessons import views

app_name = 'lessons'
urlpatterns = [
    # レッスン
    path('list/', views.get_lesson_history_list, name='history_list'),   # 一覧
    path('plan_list/', views.get_lesson_plan_list, name='plan_list'),   # 一覧
    path('add/', views.lesson_history_edit, name='history_add'),  # 登録
    path('plan_add/', views.lesson_plan_edit, name='plan_add'),  # 登録
    path('edit/<int:history_id>/', views.lesson_history_edit, name='history_edit'),  # 修正
    path('plan_edit/<int:plan_id>/', views.lesson_plan_edit, name='plan_edit'),  # 修正
]