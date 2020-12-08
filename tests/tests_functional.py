import django_webtest

from questions.models import Profile, User, Question


class PostCreationTests(django_webtest.WebTest):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user("login")
        cls.profile = Profile.objects.create(user=cls.user, nickname="nickname")
        cls.question = Question.objects.create(
            author=cls.user, text='t', title='t'
        )

    def test_registration_success(self):
        page = self.app.get('/', user=self.user)
        assert self.question.title in page

        question_page = self.app.get('/question/{}/'.format(self.question.pk),
                                     user=self.user)
        question_page.showbrowser()

        post_form = question_page.forms['form']
        post_form['text'] = 'Good question!'
        question_page = post_form.submit().follow()
        assert 'Good question!' in question_page
