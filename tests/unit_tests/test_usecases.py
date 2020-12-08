from unittest.mock import MagicMock

from django.test import TestCase
from django.contrib import auth

from questions.models import Question, Answer, Profile, User, Like
from questions.usecases import LikeQuestion, LikeAnswer


class LikeQuestionsUseCaseTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user('login', password='pass')
        cls.user = auth.authenticate(
            username='login',
            password='pass',
        )
        cls.profile = Profile.objects.create(user=cls.user, nickname='nickname')

    def test_new_like(self):
        question = Question.objects.create(author=self.user)
        use_case = LikeQuestion(self.user, 1, question.id)
        use_case._send_notification = MagicMock()

        expected_rating = question.rating + 1
        rating = use_case.run_use_case()['rating']

        self.assertEqual(expected_rating, rating)

    def test_same_value_like(self):
        question = Question.objects.create(author=self.user)
        Like.objects.like(self.profile, 1, question)
        use_case = LikeQuestion(self.user, 1, question.id)
        use_case._send_notification = MagicMock()

        expected_rating = question.rating
        rating = use_case.run_use_case()['rating']

        self.assertEqual(expected_rating, rating)

    def test_new_value_like(self):
        question = Question.objects.create(author=self.user)
        Like.objects.like(self.profile, 1, question)
        use_case = LikeQuestion(self.user, -1, question.id)
        use_case._send_notification = MagicMock()

        expected_rating = question.rating - 2
        rating = use_case.run_use_case()['rating']

        self.assertEqual(expected_rating, rating)


class LikeAnswersUseCaseTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user('login', password='pass')
        cls.user = auth.authenticate(
            username='login',
            password='pass',
        )
        cls.profile = Profile.objects.create(user=cls.user, nickname='nickname')
        cls.question = Question.objects.create(author=cls.user)

    def test_new_like(self):
        answer = Answer.objects.create(author=self.user, question=self.question)
        use_case = LikeAnswer(self.user, 1, answer.id)

        expected_rating = answer.rating + 1
        rating = use_case.run_use_case()['rating']

        self.assertEqual(expected_rating, rating)

    def test_same_value_like(self):
        answer = Answer.objects.create(author=self.user, question=self.question)
        Like.objects.like(self.profile, 1, answer)
        use_case = LikeAnswer(self.user, 1, answer.id)

        expected_rating = answer.rating
        rating = use_case.run_use_case()['rating']

        self.assertEqual(expected_rating, rating)

    def test_new_value_like(self):
        answer = Answer.objects.create(author=self.user, question=self.question)
        Like.objects.like(self.profile, 1, answer)
        use_case = LikeAnswer(self.user, -1, answer.id)

        expected_rating = answer.rating - 2
        rating = use_case.run_use_case()['rating']

        self.assertEqual(expected_rating, rating)
