import django.contrib.postgres.search as pg_search
from django.contrib.postgres.indexes import GinIndex
from django.db import models

from questions.managers import PgSearchQuestionManager
from .models import Question


class PgQuestionSearch(models.Model):
    question = models.OneToOneField(Question, related_name='pg_question',
                                    on_delete=models.CASCADE)
    search_vector_title = pg_search.SearchVectorField(null=True)
    search_vector_text = pg_search.SearchVectorField(null=True)

    objects = PgSearchQuestionManager()

    class Meta:
        required_db_vendor = 'postgresql'
        indexes = [
            GinIndex(fields=['search_vector_title', 'search_vector_text'])
        ]
