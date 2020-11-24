from datetime import datetime, timedelta

from django.test import TestCase
from django.contrib import auth

from questions.models import User, Profile, Question, Like, Tag, \
    PgQuestionSearch
from tests.request_stab import RequestStab


class LikeManagerTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user("login")
        cls.profile = Profile.objects.create(user=cls.user, nickname="nickname")

    def test_new_like(self):
        question = Question.objects.create(author=self.user)

        expected_user_rating = self.profile.rating + 1
        expected_object_rating = question.rating + 1
        like = Like.objects.like(self.profile, 1, question)

        self.assertEqual(like.value, 1)
        self.assertEqual(expected_user_rating, self.profile.rating)
        self.assertEqual(expected_object_rating, question.rating)

    def test_same_value_like(self):
        question = Question.objects.create(author=self.user)
        Like.objects.like(self.profile, 1, question)

        expected_user_rating = self.profile.rating
        expected_object_rating = question.rating

        Like.objects.like(self.profile, 1, question)

        self.assertEqual(expected_user_rating, self.profile.rating)
        self.assertEqual(expected_object_rating, question.rating)

    def test_new_value_like(self):
        question = Question.objects.create(author=self.user)
        Like.objects.like(self.profile, 1, question)

        expected_user_rating = self.profile.rating - 2
        expected_object_rating = question.rating - 2

        Like.objects.like(self.profile, -1, question)

        self.assertEqual(expected_user_rating, self.profile.rating)
        self.assertEqual(expected_object_rating, question.rating)


class ProfileManagerTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user('login', password='pass')
        cls.profile = Profile.objects.create(user=cls.user, nickname='nickname')

    def test_get_authenticated(self):
        user = auth.authenticate(
            username='login',
            password='pass',
        )

        self.assertEqual(self.profile, Profile.objects.get_authenticated(user))

    def test_get_not_authenticated(self):
        request_stab = RequestStab(self.user)
        auth.logout(request_stab)
        profile = Profile.objects.get_authenticated(request_stab.user)
        self.assertIsNone(profile)

    def test_get_best(self):
        good_user = User.objects.create_user('good')
        good_user_profile = Profile.objects.create(
            user=good_user,
            rating=100500,
        )

        expected_list = [good_user_profile, self.profile]
        users = list(Profile.objects.get_best(2))

        self.assertEqual(expected_list, users)


class TagManagerTest(TestCase):

    def test_most_popular(self):
        user = User.objects.create_user('login')

        tag1 = Tag.objects.create(text='a')
        tag2 = Tag.objects.create(text='b')
        tag3 = Tag.objects.create(text='c')

        new_question1 = Question.objects.create(author=user)
        new_question1.tags.add(tag1)
        new_question2 = Question.objects.create(author=user)
        new_question2.tags.add(tag1)
        new_question3 = Question.objects.create(author=user)
        new_question3.tags.add(tag2)
        old_question = Question.objects.create(
            author=user,
        )
        old_question.created_at = datetime.now() - timedelta(days=120)
        old_question.tags.add(tag3)
        old_question.save()

        expected = [tag1, tag2]
        most_popular = list(Tag.objects.most_popular())

        self.assertEqual(expected, most_popular)


class QuestionManagerTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user('login')

    def test_get_hot(self):
        q1 = Question.objects.create(author=self.user)
        q2 = Question.objects.create(author=self.user, rating=100500)

        expected = [q2, q1]
        hot = list(Question.objects.get_hot())

        self.assertEqual(expected, hot)

    def test_get_new(self):
        q1 = Question.objects.create(author=self.user)
        q2 = Question.objects.create(author=self.user)

        expected = [q2, q1]
        new = list(Question.objects.get_new())

        self.assertEqual(expected, new)

    def test_get_tag(self):
        tag = Tag.objects.create(text='tag')
        Question.objects.create(author=self.user)
        q2 = Question.objects.create(author=self.user)
        q2.tags.add(tag)

        expected = [q2]
        tagged = list(Question.objects.get_tag('tag'))

        self.assertEqual(expected, tagged)


class QuestionSearchTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user('login')
        cls.user.save()
        cls.q1 = Question.objects.create(
            author=cls.user,
            title='key words',
            text='long clever words',
        )
        PgQuestionSearch.objects.create(question=cls.q1,
                                        search_vector_title='key words',
                                        search_vector_text='long clever words')
        cls.q2 = Question.objects.create(
            author=cls.user,
            title='something clever',
            text='more about subject',
        )
        PgQuestionSearch.objects.create(question=cls.q2,
                                        search_vector_title='something clever',
                                        search_vector_text='more about subject')

    def test_full_word_search(self):
        expected = [self.q1]
        result = [x.question for x in Question.objects.search('key') if
                  x.rank > 0]
        self.assertEqual(expected, result)

    def test_partial_word_search(self):
        expected = [self.q1]
        result = [x.question for x in Question.objects.search('word') if
                  x.rank > 0]
        self.assertEqual(expected, result)

    def test_ranked_search(self):
        expected = [self.q2, self.q1]
        result = [x.question for x in Question.objects.search('clever')]
        self.assertEqual(expected, result)
