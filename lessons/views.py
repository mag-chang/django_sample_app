from django.shortcuts import render, get_object_or_404, redirect

from lessons.models import History, Genre
from lessons.forms import HistoryForm, GenreForm, CalculateLogicForm
from lessons.calculate_logics.logics import Logics

def get_lesson_history_list(request):
    """
    受講記録一覧を取得する
    """

    histories = History.objects.all().order_by('id')
    for history in histories:
        calculate_function = Logics().__getattribute__(history.lesson_genre.calculate_logic.logic_name)
        lesson_price = calculate_function(history.lesson_hour)
        history.__setattr__('lesson_price', lesson_price)

    return render(request,
                  'lessons/list.html',
                  {'histories': histories},
                  )

def lesson_history_edit(request, history_id=None):
    """
    受講記録を新規作成/編集する
    """

    if history_id:
        history = get_object_or_404(History, pk=history_id)
    else:
        history = History()

    if request.method == 'POST':
        form = HistoryForm(request.POST, instance=history)
        if form.is_valid():
            history = form.save(commit=False)
            history.save()
            return redirect('lessons:history_list')
    else:
        form = HistoryForm(instance=history)

    return render(
        request,
        'lessons/edit.html',
        dict(form=form, history_id=history_id)
    )


def get_lesson_genre_list(request):
    """
    ジャンル一覧を取得する
    :param request:
    :return: lesson_genreのList
    """

    genres = Genre.objects.all().order_by('id')
    return render(request,
                  'lessons/genre_list.html',
                  {'genres': genres},
                  )

def lesson_genre_edit(request, genre_id=None):
    """
    ジャンルを新規作成/編集する
    """

    if genre_id:
        genre = get_object_or_404(Genre, pk=genre_id)
    else:
        genre = Genre()

    if request.method == 'POST':
        form = GenreForm(request.POST, instance=genre)
        if form.is_valid():
            genre = form.save(commit=False)
            genre.save()
            return redirect('lessons:genre_list')
    else:
        form = GenreForm(instance=genre)

    return render(
        request,
        'lessons/genre_edit.html',
        dict(form=form, genre_id=genre_id)
    )
