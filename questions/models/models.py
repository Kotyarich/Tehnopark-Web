from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, \
    GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.shortcuts import reverse

from questions.managers import QuestionManager, TagManager, ProfileManager, \
    LikeManager


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='user',
                                on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars', default='default.jpg')
    nickname = models.CharField(max_length=100, unique=True)
    rating = models.IntegerField(default=0)

    objects = ProfileManager()

    @property
    def group_name(self):
        return 'user_{}'.format(self.id)

    def update_rating(self, add_value):
        self.rating += add_value
        self.save()


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

    objects = LikeManager()


class Question(models.Model):
    title = models.CharField(max_length=128)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(to='Tag', related_name='questions')
    rating = models.IntegerField(default=0)
    objects = QuestionManager()
    likes = GenericRelation(Like)

    def __str__(self):
        return '[pk={}] {}'.format(self.pk, self.title)

    def get_absolute_url(self):
        return reverse("question", kwargs={'id': self.pk})

    def get_user(self):
        return Profile.objects.get(user=self.author)

    def get_answers(self):
        return self.question.all().order_by('created_at')

    def update_rating(self, add_value):
        self.rating += add_value
        self.save()


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

    def update_rating(self, add_value):
        self.rating += add_value
        self.save()
