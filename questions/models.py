from django.shortcuts import reverse
from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    title = models.CharField(max_length=128)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(to='Tag', related_name='questions')

    def __str__(self):
        return '[pk={}] {}'.format(self.pk, self.title)

    def get_absolute_url(self):
        return reverse("question", kwargs={'pk': self.pk})


class Tag(models.Model):
    text = models.SlugField(unique=True)


class Answer(models.Model):
    pass


class Profile(models.Model):
    pass


class Like(models.Model):
    pass
