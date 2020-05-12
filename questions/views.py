import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
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


@login_required(login_url='login', redirect_field_name='redirect_to')
def like(request):
    if request.method == 'POST':
        value = int(request.POST.get('value'))
        pk = request.POST.get('pk')
        profile = Profile.objects.get_authenticated(request.user)
        q = Question.objects.get(id=pk)
        rating = Like.objects.like(profile, value, q)
        response_data = {'result': rating}
        return HttpResponse(
            json.dumps(response_data),
            content_type='application/json'
        )


def index(request):
    questions_list = Question.objects.get_new()
    questions, paginator = paginate(questions_list, request)
    profile = Profile.objects.get_authenticated(request.user)

    return render(
        request,
        'index.html',
        {'objects': questions, 'profile': profile}
    )


def hot(request):
    questions_list = Question.objects.get_hot()
    questions, paginator = paginate(questions_list, request)
    profile = Profile.objects.get_authenticated(request.user)

    return render(
        request,
        'index.html',
        {'objects': questions, 'profile': profile},
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
    profile = Profile.objects.get_authenticated(request.user)

    return render(
        request,
        'ask.html',
        {'form': form, 'profile': profile}
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
    profile = Profile.objects.get_authenticated(request.user)

    return render(
        request,
        'settings.html',
        {'form': form, 'profile': profile}
    )


def question(request, id):
    question = get_object_or_404(Question, pk=id)
    answers_list = Answer.objects.filter(question=question)
    answers, paginator = paginate(answers_list, request)
    if request.POST:
        form = AnswerForm(request.POST)
        if form.is_valid():
            form.save(request.user, question)
            redirect_to = question.get_absolute_url() \
                          + '?page={}#form'.format(paginator.num_pages)
            return redirect(redirect_to)

    form = AnswerForm()
    profile = Profile.objects.get_authenticated(request.user)

    return render(request, 'question.html', {
        'objects': answers,
        'question': question,
        'form': form,
        'profile': profile
    })


def tag(request, tag):
    questions_list = Question.objects.get_tag(tag)
    questions, paginator = paginate(questions_list, request)
    profile = Profile.objects.get_authenticated(request.user)

    return render(
        request,
        'tagsearch.html',
        {'objects': questions, 'tag': tag,
         'profile': profile}
    )


def search(request):
    query = request.GET.get('query')
    ranked_top = Question.objects.search(query)[:5]
    results = [{'id': x.question.pk, 'title': x.question.title} for x in
               ranked_top]

    return HttpResponse(
        json.dumps({'results': results}),
        content_type='application/json',
    )
