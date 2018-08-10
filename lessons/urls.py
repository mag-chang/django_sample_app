from django.urls import path
from lessons import views

app_name = 'lessons'
urlpatterns = [
    # レッスン
    path('list/', views.get_lesson_history_list, name='history_list'),   # 一覧
    path('genre_list/', views.get_lesson_genre_list, name='genre_list'),   # 一覧
    path('add/', views.lesson_history_edit, name='history_add'),  # 登録
    path('genre_add/', views.lesson_genre_edit, name='genre_add'),  # 登録
    path('edit/<int:history_id>/', views.lesson_history_edit, name='history_edit'),  # 修正
    path('genre_edit/<int:genre_id>/', views.lesson_genre_edit, name='genre_edit'),  # 修正
]