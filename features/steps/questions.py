from behave import *
from django.contrib.auth.models import User

from questions.models import Profile, Question

use_step_matcher("re")


@given("I am a visitor")
def step_impl(context):
    user = User.objects.create_user("login", password='1234')
    user.save()
    profile = Profile.objects.create(user=user, nickname="nickname")
    profile.save()

    br = context.browser
    br.get(context.base_url + '/login/')
    br.find_element_by_name('username').send_keys('login')
    br.find_element_by_name('password').send_keys('1234')
    br.find_element_by_xpath("//button[@type='submit']").click()


@given("exists questions")
def step_impl(context):
    user = User.objects.get(username='login')
    question = Question.objects.create(author=user, text='t', title='t')
    question.save()


@when('I create answer "Good question!" to question')
def step_impl(context):
    br = context.browser
    question = Question.objects.get(title='t')
    br.get(context.base_url + '/question/{}/'.format(question.pk))
    br.find_element_by_name('text').send_keys('Good question!')
    br.find_element_by_xpath("//button[contains(.,'Answer')]").click()


@then('I should see "Good question!" in page')
def step_impl(context):
    br = context.browser
    assert 'Good question!' in br.page_source
