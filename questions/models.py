from datetime import timedelta, datetime

from django.db.models import Count, Q
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, \
    GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.indexes import GinIndex
import django.contrib.postgres.search as pg_search
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank
from django.db import models
from django.shortcuts import reverse


class QuestionManager(models.Manager):
    def get_hot(self):
        return self.order_by('-rating')

    def get_new(self):
        return self.order_by('-created_at')

    def get_tag(self, tag):
        return self.filter(tags__text=tag)

    def search(self, query):
        search_query = SearchQuery(query)
        title_vector = SearchVector('search_vector_title', weight='A')
        text_vector = SearchVector('search_vector_text', weight='C')
        rank = SearchRank(title_vector + text_vector, search_query)
        return self.annotate(rank=rank).order_by('-rank')

    def like(self, user, value, pk):
        profile = Profile.objects.get(user=user)
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
        except Like.DoesNotExist:
            like = Like(value=value, user=user, content_object=question)
            like.save()
            profile.rating += value
            question.rating += value
            profile.save()
            question.save()


class TagManager(models.Manager):
    def most_popular(self):
        """Tags with biggest amount of questions in last 3 months"""
        three_months_ago = datetime.today() - timedelta(days=90)
        return self.annotate(num_questions=Count(
            'questions', filter=Q(questions__created_at=three_months_ago))
        ).order_by('-num_questions')


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='user',
                                on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars', default='default.jpg')
    nickname = models.CharField(max_length=100, unique=True)
    rating = models.IntegerField(default=0)


class Like(models.Model):
    VALUES = (
        ('UP', 1),
        ('DOWN', -1),
    )
    value = models.SmallIntegerField(choices=VALUES)
    user = models.ForeignKey(User, related_name='liker',
                             on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class Question(models.Model):
    title = models.CharField(max_length=128)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(to='Tag', related_name='questions')
    rating = models.IntegerField(default=0)
    objects = QuestionManager()
    likes = GenericRelation(Like)

    search_vector_title = pg_search.SearchVectorField(null=True)
    search_vector_text = pg_search.SearchVectorField(null=True)

    class Meta:
        indexes = [
            GinIndex(fields=['search_vector_title', 'search_vector_text'])
        ]

    def __str__(self):
        return '[pk={}] {}'.format(self.pk, self.title)

    def get_absolute_url(self):
        return reverse("question", kwargs={'id': self.pk})

    def get_user(self):
        return Profile.objects.get(user=self.author)


class Tag(models.Model):
    text = models.SlugField(unique=True)
    objects = TagManager()

    def get_absolute_url(self):
        return reverse("tag", kwargs={'tag': self.text})


class Answer(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='question',
                                 on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    likes = GenericRelation(Like)

    def __str__(self):
        return self.text

    def get_user(self):
        return Profile.objects.get(user=self.author)
