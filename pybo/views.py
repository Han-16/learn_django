from django.shortcuts import render, get_object_or_404, redirect
# from django.http import HttpResponseNotAllowed
from .models import Question, Answer
from django.utils import timezone
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

def index(request):
    page = request.GET.get('page', '1')
    question_list = Question.objects.order_by('-create_date')
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)
    context = { 'question_list' : page_obj }
    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    # question = Question.objects.get(id = question_id)
    question = get_object_or_404(Question, pk = question_id)
    context = { 'question' : question } # key값이 template에서 사용할 변수이름, value 값이 파이썬 변수
    return render(request, "pybo/question_detail.html", context)

@login_required(login_url='common:login')
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)     # QuestionForm은 question 데이터베이스와 연결되어있음
            question.author = request.user
            question.create_date = timezone.now()  # 그래서 바로 저장을 하게되면 create_date가 없어서 오류가 남.
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    context = { 'form' : form }
    return render(request, 'pybo/question_form.html',
                  context)

@login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없는데용?')
        return redirect('pybo:detail', question_id=question.id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()  # 수정일시 저장
            question.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, "삭제 권한 없는걸요?")
        return redirect('pybo:detail', question_id = question.id)
    question.delete()
    return redirect('pybo:index')


@login_required(login_url='common:login')
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)

    # question.answer_set.create(content=request.POST.get('content'), create_date = timezone.now())
    # return redirect('pybo:detail', question_id = question.id)
@login_required(login_url="common:login")
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk = answer_id)
    if request.user != answer.author:
        messages.error(request, "당신, 수정 권한이 없네만?")
        return redirect('pybo:detail', question_id = answer.question.id)
    if request.method == "POST":
        form = AnswerForm(request.POST, instance = answer)
        if form.is_valid():
            answer = form.save(commit = False)
            answer.modify_date = timezone.now()
            answer.save()
            return redirect("pybo:detail", question_id = answer.question.id)
    else:
        form = AnswerForm(instance = answer)
    context = { "answer" : answer, "form" : form }
    return render(request, "pybo/answer_form.html", context)

@login_required(login_url="common:login")
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, "당신, 삭제 권한이 없네만?")
    else:
        answer.delete()
    return redirect('pybo:detail', question_id = answer.question.id)