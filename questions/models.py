from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.db import models
from django.contrib.auth.models import User


class QuestionManager(models.Manager):
    def get_hot(self):
        return self.order_by('-rating')

    def get_new(self):
        return self.order_by('created_at')

    def get_tag(self, tag):
        return self.filter(tags__text=tag)


class Question(models.Model):
    title = models.CharField(max_length=128)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(to='Tag', related_name='questions')
    rating = models.IntegerField(default=0)
    objects = QuestionManager()

    def __str__(self):
        return '[pk={}] {}'.format(self.pk, self.title)

    def get_absolute_url(self):
        return reverse("question", kwargs={'id': self.pk})


class Tag(models.Model):
    text = models.SlugField(unique=True)

    def get_absolute_url(self):
        return reverse("tag", kwargs={'tag': self.text})


class Answer(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='question', on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars')
    nickname = models.CharField(max_length=100, unique=True)


class QuestionLike(models.Model):
    VALUES = (
        ('UP', 1),
        ('DOWN', -1),
    )
    value = models.SmallIntegerField(choices=VALUES)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')