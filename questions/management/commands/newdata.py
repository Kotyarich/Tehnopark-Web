import random

from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from questions.models import Question as Poll
from questions.models import Question, User, Tag, Answer, QuestionLike, Profile
from faker import Faker
from random import randint

faker = Faker()


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('--users', type=int, default=0)
        parser.add_argument('--questions', type=int, default=0)

    def handle(self, *args, **options):
        self.create_tags()
        self.create_profiles()
        self.create_questions()
        self.create_answers()

    def create_tags(self):
        if Tag.objects.count() > 0:
            return

        for i in range(30):
            tag = Tag.objects.create(text=faker.word() + str(i))
            tag.save()

    def create_profiles(self):
        if User.objects.count() > 0:
             return

        user = User.objects.create_user('user1', 'user@mail.ru', '1234')
        user.save()
        p = Profile.objects.create(user=user)
        p.save()

    def create_questions(self):
        if Question.objects.count() > 0:
            return

        tags = Tag.objects.all()
        for i in range(1000):
            question = Question.objects.create(title=faker.sentence(),
                                               text=faker.text(),
                                               author=User.objects.first(),
                                               rating=random.randint(-2, 20))
            for j in range(3):
                tag = random.choice(tags)
                question.tags.add(tag)
            question.save()

    def create_answers(self):
        if Answer.objects.count() > 0:
            return
        for question in Question.objects.all():
            for i in range(random.randint(1, 20)):
                a = Answer.objects.create(text=faker.text(), question=question, author=User.objects.first())
                a.save()
