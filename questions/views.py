from django.shortcuts import render
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from faker import Faker
from questions.models import Question

fake = Faker()


def new_questions(request):
    questions = Question.objects.all().order_by('-created_at')
    return render(request, 'questions_list.html', {
        'questions': questions
    })


def q(request, pk):
    question = Question.objects.get(pk=pk)
    return render(request, 'list_question.html', {
        'questions': question
    })


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
    questions_list = [
        {
            'id': id,
            'title': fake.sentence(),
            'text': fake.text(),
        } for id in range(105)
    ]

    questions, paginator = paginate(questions_list, request)

    return render(request, 'index.html', {'questions': questions})


def hot(request):
    questions_list = [
        {
            'id': id,
            'title': fake.sentence(),
            'text': fake.text(),
        } for id in range(9)
    ]

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


def question(request):
    answers_list = [
        {
            'id': id,
            'title': fake.sentence(),
            'text': fake.text(),
        } for id in range(10)
    ]
    answers, paginator = paginate(answers_list, request)
    return render(request, 'question.html', {'questions': answers})


def tag(request):
    questions_list = [
        {
            'id': id,
            'title': fake.sentence(),
            'text': fake.text(),
        } for id in range(10)
    ]
    questions, paginator = paginate(questions_list, request)
    return render(request, 'tagsearch.html', {'questions': questions})
