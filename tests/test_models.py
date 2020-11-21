from unittest.mock import MagicMock

from django.test import TestCase

from questions.models import Profile, Question, User, Answer, Tag


class ProfileModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user("login")
        cls.profile = Profile.objects.create(user=cls.user, nickname="nickname")

    def test_first_name_max_length(self):
        expected_max_length = 100

        max_length = self.profile._meta.get_field('nickname').max_length

        self.assertEquals(max_length, expected_max_length)

    def test_group_name(self):
        profile_id = self.profile.id
        expected_group_name = "user_{}".format(profile_id)

        self.assertEqual(expected_group_name, self.profile.group_name)

    def test_update_rating(self):
        self.profile.save = MagicMock()
        add_value = 1
        expected_rating = self.profile.rating + add_value

        self.profile.update_rating(add_value)

        self.profile.save.assert_called_once()
        self.assertEqual(expected_rating, self.profile.rating)


class QuestionModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user("login")
        cls.question = Question.objects.create(author=cls.user)

    def test_first_name_max_length(self):
        expected_max_length = 128

        max_length = self.question._meta.get_field('title').max_length

        self.assertEquals(max_length, expected_max_length)

    def test_to_string(self):
        self.question.title = 'title'

        expected_string = '[pk={}] {}'.format(self.question.id, 'title')

        self.assertEqual(expected_string, str(self.question))

    def test_get_absolute_url(self):
        question_id = self.question.id
        self.assertEqual(self.question.get_absolute_url(),
                         '/question/{}/'.format(question_id))

    def test_get_user(self):
        profile = Profile.objects.create(user=self.user, nickname='nickname')
        self.assertEqual(self.question.get_user(), profile)

    def test_get_answers(self):
        answers = [
            Answer.objects.create(
                author=self.question.author, question=self.question
            ) for _ in range(2)
        ]

        self.assertEqual(list(self.question.get_answers()), answers)

    def test_update_rating(self):
        self.question.save = MagicMock()
        add_value = 1
        expected_rating = self.question.rating + add_value

        self.question.update_rating(add_value)

        self.question.save.assert_called_once()
        self.assertEqual(expected_rating, self.question.rating)


class TagModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.tag = Tag.objects.create(text='tag')

    def test_get_absolute_url(self):
        expected = '/tag/{}'.format(self.tag.text)
        self.assertEqual(self.tag.get_absolute_url(), expected)


class AnswerModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user("login")
        cls.question = Question.objects.create(author=cls.user)
        cls.answer = Answer.objects.create(author=cls.user,
                                           question=cls.question,
                                           text='answer')

    def test_to_string(self):
        expected_string = self.answer.text
        self.assertEqual(expected_string, str(self.answer))

    def test_get_user(self):
        profile = Profile.objects.create(user=self.user, nickname='nickname')
        self.assertEqual(self.answer.get_user(), profile)

    def test_update_rating(self):
        self.answer.save = MagicMock()
        add_value = 1
        expected_rating = self.answer.rating + add_value

        self.answer.update_rating(add_value)

        self.answer.save.assert_called_once()
        self.assertEqual(expected_rating, self.answer.rating)
