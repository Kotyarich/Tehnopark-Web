from django.shortcuts import render, get_object_or_404
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from faker import Faker
from questions.models import Question, Answer

fake = Faker()


def paginate(objects_list, request):
    paginator = Paginator(objects_list, 10)
    page = request.GET.get('page')
    try:
        objects_page = paginator.page(page)
    except PageNotAnInteger:
        objects_page = paginator.page(1)
    except EmptyPage:
        objects_page = paginator.page(paginator.num_pages)

    return objects_page, paginator


# Create your views here.
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


def question(request, id):
    question = get_object_or_404(Question, pk=id)
    answers_list = Answer.objects.filter(question=question)
    answers, paginator = paginate(answers_list, request)

    return render(request, 'question.html', {'questions': answers, 'question': question})


def tag(request, tag):
    questions_list = Question.objects.get_tag(tag)
    questions, paginator = paginate(questions_list, request)

    return render(request, 'tagsearch.html', {'questions': questions, 'tag': tag})
