# Generated by Django 2.1.2 on 2018-10-23 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0002_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(related_name='questions', to='questions.Tag'),
        ),
    ]
