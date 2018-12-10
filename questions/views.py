from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import admin, auth
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import path, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from faker import Faker
from questions.models import Question, Answer
from questions.forms import LoginForm, RegisterForm, EditForm

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


def index(request):
    questions_list = Question.objects.get_new()
    questions, paginator = paginate(questions_list, request)

    return render(request, 'index.html', {'objects': questions})


def hot(request):
    questions_list = Question.objects.get_hot()
    questions, paginator = paginate(questions_list, request)

    return render(request, 'index.html', {'objects': questions})


def login(request):
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            cdata = form.cleaned_data
            user = auth.authenticate(
                username=cdata['username'],
                password=cdata['password']
            )
            if user is not None:
                auth.login(request, user)
                return redirect(request.GET.get('redirect_to'))
            form.add_error('username', "Wrong username or password")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('redirect_to'))


def register(request):
    if request.POST:
        form = RegisterForm(request.POST)
        if form.is_valid():
            cdata = form.cleaned_data
            user = User.objects.create_user(
                cdata['nickname'],
                cdata['email'],
                cdata['password']
            )
            user.save()
            print(cdata['nickname'], cdata['email'], cdata['password'])
            return redirect('new_questions')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


@login_required(login_url='login', redirect_field_name='redirect_to')
def ask(request):
    return render(request, 'ask.html')


@login_required(login_url='login', redirect_field_name='redirect_to')
def settings(request):
    form = EditForm()
    return render(request, 'settings.html', {'form': form})


def question(request, id):
    question = get_object_or_404(Question, pk=id)
    answers_list = Answer.objects.filter(question=question)
    answers, paginator = paginate(answers_list, request)

    return render(request, 'question.html', {'objects': answers, 'question': question})


def tag(request, tag):
    questions_list = Question.objects.get_tag(tag)
    questions, paginator = paginate(questions_list, request)

    return render(request, 'tagsearch.html', {'objects': questions, 'tag': tag})
