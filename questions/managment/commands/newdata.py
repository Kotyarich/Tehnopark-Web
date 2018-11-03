from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from questions.models import Question as Poll
from questions.models import Question, User
from faker import Faker
from random import randint

faker = Faker()


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('--users', type=int, default=0)
        parser.add_argument('--questions', type=int, default=0)

    def handle(self, *args, **options):
        for _ in range(options.get("users")):
            try:
                User.objects.create_user(faker.user_name())
            except IntegrityError:
                pass
        uids = User.objects.va
        for _ in range(options.get("")):
            pass
