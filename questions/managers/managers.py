import logging
from abc import ABC
from datetime import timedelta, datetime

from django.contrib.postgres.search import SearchQuery, SearchVector
from django.db import models as django_models
from django.db.models import Count

logger = logging.getLogger(__name__)


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

        return pg_manager.most_similar(result_vector, search_query)

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
        return self.filter(tags__text=tag).order_by('-rating')

    def search(self, query):
        fields = (('title', 'A'), ('text', 'C'))
        pg_manager = self.model.pg_question.get_queryset().model.objects
        return self._base_search(query, fields, pg_manager)


class TagManager(django_models.Manager):
    def most_popular(self):
        """Tags with biggest amount of questions in last 3 months"""
        three_months_ago = datetime.now() - timedelta(days=90)
        return self.filter(questions__created_at__gte=three_months_ago) \
            .annotate(num_questions=Count('questions')) \
            .order_by('-num_questions')


class ProfileManager(django_models.Manager):
    def get_authenticated(self, user):
        if user.is_authenticated:
            return self.get(user=user)
        logger.info('User id={} is not authenticated'.format(user.id))
        return None

    def get_best(self, limit):
        best_users = self.order_by('-rating')[:limit]
        return best_users


class LikeManager(django_models.Manager):
    def like(self, profile, value, content_object):
        try:
            like = self.get(user=profile.user, object_id=content_object.id)
            if like.value != value:
                add_value = value * 2
                like.value = value
                like.save()
                logger.info('Like id={} updated'.format(like.id))
            else:
                add_value = 0
        except self.model.DoesNotExist:
            like = self.create(value=value, user=profile.user,
                               content_object=content_object)
            add_value = value
            like.save()
            logger.info('Like id={} created'.format(like.id))

        author_profile = content_object.author.user

        if add_value != 0:
            author_profile.update_rating(add_value)
            content_object.update_rating(add_value)

        return like
