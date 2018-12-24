import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import admin, auth
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import path, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from faker import Faker
from questions.forms import *
from questions.models import Like

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


def current_profile(user):
    if user.is_authenticated:
        return Profile.objects.get(user=user)
    return None


@login_required(login_url='login', redirect_field_name='redirect_to')
def like(request):
    if request.method == 'POST':
        value = int(request.POST.get('value'))
        pk = request.POST.get('pk')
        print(pk)
        question = Question.objects.get(pk=pk)
        try:
            like = question.likes.get(user=request.user)
            if like.value != value:
                question.rating += value * 2
                like.value = value
                like.save()
                question.save()
        except Like.DoesNotExist:
            like = Like(value=value, user=request.user, content_object=question)
            like.save()
            question.rating += value
            question.save()
        response_data = {'result': question.rating}
        return HttpResponse(
            json.dumps(response_data),
            content_type='application/json'
        )


def index(request):
    questions_list = Question.objects.get_new()
    questions, paginator = paginate(questions_list, request)

    return render(
        request,
        'index.html',
        {'objects': questions, 'profile': current_profile(request.user)}
    )


def hot(request):
    questions_list = Question.objects.get_hot()
    questions, paginator = paginate(questions_list, request)

    return render(
        request,
        'index.html',
        {'objects': questions, 'profile': current_profile(request.user)},
    )


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
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(request)
            return redirect('new_questions')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


@login_required(login_url='login', redirect_field_name='redirect_to')
def ask(request):
    if request.POST:
        form = QuestionForm(request.POST)
        if form.is_valid():
            q = form.save(request.user)
            return redirect(q.get_absolute_url())
    else:
        form = QuestionForm()

    return render(
        request,
        'ask.html',
        {'form': form, 'profile': current_profile(request.user)}
    )


@login_required(login_url='login', redirect_field_name='redirect_to')
def settings(request):
    if request.POST:
        form = EditForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(request)
            return redirect('settings')
    else:
        form = EditForm()
    return render(
        request,
        'settings.html',
        {'form': form, 'profile': current_profile(request.user)}
    )


def question(request, id):
    question = get_object_or_404(Question, pk=id)
    answers_list = Answer.objects.filter(question=question)
    answers, paginator = paginate(answers_list, request)
    if request.POST:
        form = AnswerForm(request.POST)
        if form.is_valid():
            form.save(request.user, question)
            redirect_to = question.get_absolute_url()\
                          + '?page={}#form'.format(paginator.num_pages)
            return redirect(redirect_to)

    form = AnswerForm()
    return render(request, 'question.html', {
        'objects': answers,
        'question': question,
        'form': form,
        'profile': current_profile(request.user)
    })


def tag(request, tag):
    questions_list = Question.objects.get_tag(tag)
    questions, paginator = paginate(questions_list, request)

    return render(
        request,
        'tagsearch.html',
        {'objects': questions, 'tag': tag, 'profile': current_profile(request.user)}
    )
