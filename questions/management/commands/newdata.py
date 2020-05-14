import random

from django.core.management.base import BaseCommand
from faker import Faker

from questions.models import Question, User, Tag, Answer, Like, Profile

faker = Faker()


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('--users', type=int, default=0)
        parser.add_argument('--questions', type=int, default=0)

    def handle(self, *args, **options):
        self.create_tags()
        self.create_profiles()
        users = User.objects.all()
        self.create_questions()
        self.create_answers()
        questions = Question.objects.all()
        answers = Answer.objects.all()
        self.create_likes(users, questions, answers)

    def create_tags(self):
        # if Tag.objects.count() > 0:
        #     return

        for i in range(40):
            tag = Tag.objects.create(text=faker.word() + str(i))
            tag.save()

    def create_profiles(self):
        # if User.objects.count() > 0:
        #     return

        user = User.objects.create_superuser('user1', 'user@mail.ru', '1234')
        user.save()
        p = Profile.objects.create(user=user, nickname='nickname')
        p.save()
        for i in range(40):
            user = User.objects.create_user(
                username=str(i) + str(i),
                password='pass{}'.format(i),
                email=str(i) + faker.email())
            user.save()
            p = Profile.objects.create(user=user, nickname='nickname' + str(i))
            p.save()

    def create_questions(self):
        # if Question.objects.count() > 0:
        #     return

        tags = Tag.objects.all()
        for i in range(101):
            question = Question.objects.create(
                title=faker.sentence(),
                text=faker.text(),
                author=User.objects.first(),
                rating=0
            )

            for j in range(3):
                tag = random.choice(tags)
                question.tags.add(tag)
            question.save()

    def create_answers(self):
        # if Answer.objects.count() > 0:
        #     return
        for question in Question.objects.all():
            for i in range(random.randint(1, 25)):
                a = Answer.objects.create(text=faker.text(), question=question,
                                          author=User.objects.first())
                a.save()

    def create_likes(self, users, questions, answers):
        for user in users:
            qs = random.sample(list(questions), 40)
            for q in qs:
                value = random.choice([1, -1])
                like = Like(value=value, user=user, content_object=q)
                like.save()
                like.content_object.rating += like.value
                like.content_object.save(update_fields=['rating'])

            ans = random.sample(list(answers), 100)
            for a in ans:
                value = random.choice([1, -1])
                like = Like(value=value, user=user, content_object=a)
                like.save()
                like.content_object.rating += like.value
                like.content_object.save(update_fields=['rating'])
