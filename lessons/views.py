from django.shortcuts import render, get_object_or_404, redirect

from lessons.models import History, Plan
from lessons.forms import HistoryForm, PlanForm, CalculateLogicForm

def get_lesson_history_list(request):
    """
    受講記録一覧を取得する
    :param request:
    :return: lesson_historyのList
    """

    histories = History.objects.all().order_by('id')
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


def get_lesson_plan_list(request):
    """
    ジャンル一覧を取得する
    :param request:
    :return: lesson_planのList
    """

    plans = Plan.objects.all().order_by('id')
    # [plan.started_month = plan.started_month for plan in plans]
    return render(request,
                  'lessons/plan_list.html',
                  {'plans': plans},
                  )

def lesson_plan_edit(request, plan_id=None):
    """
    ジャンルを新規作成/編集する
    """

    if plan_id:
        plan = get_object_or_404(Plan, pk=plan_id)
    else:
        plan = Plan()

    if request.method == 'POST':
        form = PlanForm(request.POST, instance=plan)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.save()
            return redirect('lessons:plan_list')
    else:
        form = PlanForm(instance=plan)

    return render(
        request,
        'lessons/plan_edit.html',
        dict(form=form, plan_id=plan_id)
    )
