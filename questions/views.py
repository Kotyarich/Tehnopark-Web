from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from questions.models import Question, Answer


def paginate(objects_list, request):
    items_per_page = 10
    paginator = Paginator(objects_list, items_per_page)
    page = request.GET.get('page')
    try:
        objects_page = paginator.page(page)
    except PageNotAnInteger:
        objects_page = paginator.page(1)
    except EmptyPage:
        objects_page = paginator.page(paginator.num_pages)

    return objects_page, paginator


def index(request):
    questions_list = Question.objects.get_new()
    questions, paginator = paginate(questions_list, request)

    return render(request, 'index.html', {'questions': questions})


def hot(request):
    questions_list = Question.objects.get_hot()
    questions, paginator = paginate(questions_list, request)

    return render(request, 'index.html', {'questions': questions})


def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')


def ask(request):
    return render(request, 'ask.html')


def settings(request):
    return render(request, 'settings.html')


def question(request, pk):
    question_obj = get_object_or_404(Question, pk=pk)
    answers_list = Answer.objects.filter(question=question_obj)
    answers, paginator = paginate(answers_list, request)

    return render(request,
                  'question.html',
                  {'questions': answers, 'question': question_obj})


def tag(request, tag):
    questions_list = Question.objects.get_tag(tag)
    questions, paginator = paginate(questions_list, request)

    return render(request,
                  'tagsearch.html',
                  {'questions': questions, 'tag': tag})
