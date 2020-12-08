from http import HTTPStatus
from unittest.mock import patch

from django.test import TestCase
from questions.models import Profile, User, Question, Like


class RegistrationTests(TestCase):
    def test_registration_success(self):
        user_data = {
            'email': 'email@mail.ru',
            'nickname': 'username',
            'password': '123456',
            'repeat_password': '123456',
        }

        response = self.client.post('/signup/', data=user_data)

        self.assertRedirects(response, '/')
        global created_user
        try:
            created_user = User.objects.get(username=user_data['nickname'])
        except User.DoesNotExist:
            self.assertTrue(False, 'user haven\'t been created')
        self.assertEqual(created_user.email, user_data['email'])

    def test_registration_already_exists(self):
        User.objects.create(
            username='username', email='email@mail.ru', password='123456'
        )
        user_data = {
            'email': 'email@mail.ru',
            'nickname': 'username',
            'password': '123456',
            'repeat_password': '123456',
        }

        response = self.client.post('/signup/', data=user_data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRaises(Profile.DoesNotExist,
                          Profile.objects.get,
                          nickname=user_data['nickname'])


@patch("questions.usecases.LikeQuestion._send_notification", autospec=True)
class LikeQuestionTests(TestCase):
    def test_like_success(self, mock_send_notification):
        user = User.objects.create(username='user')
        Profile.objects.create(user=user, nickname='user').save()
        question = Question.objects.create(author=user, title='t', text='t')
        question.save()
        like_data = {'pk': question.pk, 'value': 1}

        self.client.force_login(user)
        response = self.client.post('/like/', data=like_data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        global created_like
        try:
            created_like = Like.objects.get(object_id=question.pk)
        except Like.DoesNotExist:
            self.assertTrue(False, 'like haven\'t been created')
        self.assertEqual(created_like.value, like_data['value'])
        self.assertTrue(mock_send_notification.called)

    def test_like_already_exist(self, mock_send_notification):
        user = User.objects.create(username='user')
        profile = Profile.objects.create(user=user, nickname='user')
        profile.save()
        question = Question.objects.create(author=user, title='t', text='t')
        question.save()
        like = Like.objects.like(profile, 1, question)
        question_rating = like.content_object.rating
        like_data = {'pk': question.pk, 'value': 1}

        self.client.force_login(user)
        response = self.client.post('/like/', data=like_data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        global created_like
        try:
            created_like = Like.objects.get(object_id=question.pk)
        except Like.DoesNotExist:
            self.assertTrue(False, 'like haven\'t been created')
        self.assertEqual(created_like.value, like_data['value'])
        self.assertEqual(created_like.pk, like.pk)
        updated_question = Question.objects.get(pk=question.pk)
        self.assertEqual(updated_question.rating, question_rating)
        self.assertFalse(mock_send_notification.called)
