import json
import math

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, FormView
from django.views.generic.base import ContextMixin, RedirectView, View
from django.views.generic.detail import SingleObjectMixin

from questions.forms import *
from questions.models import Like


class ProfileMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get_authenticated(self.request.user)
        context['profile'] = profile
        return context


class QuestionsList(ProfileMixin, ListView):
    template_name = 'index.html'
    context_object_name = 'objects'
    paginate_by = 10
    queryset = Question.objects.get_new()


class HotQuestionsList(QuestionsList):
    queryset = Question.objects.get_hot()


class TaggedQuestionsList(QuestionsList):
    template_name = 'tagsearch.html'

    def get_queryset(self):
        chosen_tag = self.kwargs['tag']
        return Question.objects.get_tag(chosen_tag)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.kwargs['tag']
        return context


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm

    def get_success_url(self):
        return self.request.GET.get('redirect_to')

    def get_form_kwargs(self):
        kwargs = super(LoginView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class LogoutView(RedirectView):
    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        auth.logout(self.request)
        return self.request.GET.get('redirect_to')


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = '/'

    def form_valid(self, form):
        form.save(self.request)
        return super(RegisterView, self).form_valid(form)


class AskView(LoginRequiredMixin, ProfileMixin, FormView):
    template_name = 'ask.html'
    form_class = QuestionForm
    login_url = 'login'
    redirect_field_name = 'redirect_to'
    question = None

    def get_success_url(self):
        return self.question.get_absolute_url()

    def form_valid(self, form):
        self.question = form.save(self.request.user)
        return super(AskView, self).form_valid(form)


class SettingsView(LoginRequiredMixin, ProfileMixin, FormView):
    template_name = 'settings.html'
    form_class = EditForm
    success_url = '/settings/'
    login_url = 'login'
    redirect_field_name = 'redirect_to'

    def form_valid(self, form):
        form.save(self.request)
        return super(SettingsView, self).form_valid(form)


class LikeView(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'redirect_to'

    @staticmethod
    def post(request):
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


class QuestionDisplay(ProfileMixin, SingleObjectMixin, ListView):
    paginate_by = 10
    template_name = 'question.html'
    object = None

    def get(self, request, *args, **kwargs):
        self.object = get_object_or_404(Question, pk=self.kwargs['id'])
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['objects'] = context.pop('object_list')
        context['question'] = self.object
        context['form'] = AnswerForm()
        return context

    def get_queryset(self):
        return self.object.get_answers()


class QuestionsAnswer(SingleObjectMixin, FormView):
    template_name = 'question.html'
    form_class = AnswerForm
    object = None
    pagesCount = None

    def form_valid(self, form):
        form.save(self.request.user, self.object)
        return super(QuestionsAnswer, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = get_object_or_404(Question, pk=self.kwargs['id'])
        self.pagesCount = math.ceil(self.object.question.all().count() / 10)
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        args = '?page={}#form'.format(self.pagesCount)
        return self.object.get_absolute_url() + args


class QuestionView(View):
    @staticmethod
    def get(request, *args, **kwargs):
        view = QuestionDisplay.as_view()
        return view(request, *args, **kwargs)

    @staticmethod
    def post(request, *args, **kwargs):
        view = QuestionsAnswer.as_view()
        return view(request, *args, **kwargs)


class SearchView(View):
    @staticmethod
    def get(request):
        query = request.GET.get('query')
        ranked_top = Question.objects.search(query)[:5]
        results = [{'id': x.question.pk, 'title': x.question.title} for x in
                   ranked_top]

        return HttpResponse(
            json.dumps({'results': results}),
            content_type='application/json',
        )
