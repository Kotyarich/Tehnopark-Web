from abc import ABC
from datetime import timedelta, datetime

from django.db import models as django_models
from django.db.models import Count, Q
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank

from questions import models


class FulltextSearchManager(django_models.Manager, ABC):
    @staticmethod
    def __postgres_search(query, fields, pg_manager):
        search_query = SearchQuery(query)

        result_vector = None
        for field in fields:
            if len(field) > 1:
                vector = SearchVector('search_vector_' + field[0],
                                      weight=field[1])
            else:
                vector = SearchVector('search_vector_' + field[0])

            if result_vector is None:
                result_vector = vector
            else:
                result_vector += vector

        rank = SearchRank(result_vector, search_query)
        ranked_result = pg_manager.annotate(rank=rank).order_by('-rank')
        return ranked_result.select_related('question')

    def __common_search(self, query, fields):
        query_sets = []
        sorted_fields = sorted(fields, key=lambda item: item[1])
        for field in sorted_fields:
            kwargs = {field[0] + '__contains': query}
            query_sets.append(self.filter(**kwargs))

        return query_sets[0].union(*query_sets[1:])

    def _base_search(self, query, fields, pg_manager):
        if self.db == 'default':
            return self.__postgres_search(query, fields, pg_manager)
        else:
            return self.__common_search(query, fields)


class QuestionManager(FulltextSearchManager):
    def get_hot(self):
        return self.order_by('-rating')

    def get_new(self):
        return self.order_by('-created_at')

    def get_tag(self, tag):
        return self.filter(tags__text=tag)

    def search(self, query):
        fields = (('title', 'A'), ('text', 'C'))
        return self._base_search(query, fields, models.PgQuestionSearch.objects)

    def like(self, user, value, pk):
        profile = models.Profile.objects.get(user=user)
        question = self.get(pk=pk)
        try:
            like = question.likes.get(user=user)
            if like.value != value:
                profile.rating += value * 2
                question.rating += value * 2
                like.value = value
                like.save()
                question.save()
                profile.save()
        except models.Like.DoesNotExist:
            like = models.Like(value=value, user=user, content_object=question)
            like.save()
            profile.rating += value
            question.rating += value
            profile.save()
            question.save()
        return question.rating


class TagManager(django_models.Manager):
    def most_popular(self):
        """Tags with biggest amount of questions in last 3 months"""
        three_months_ago = datetime.today() - timedelta(days=90)
        return self.annotate(num_questions=Count(
            'questions', filter=Q(questions__created_at=three_months_ago))
        ).order_by('-num_questions')
