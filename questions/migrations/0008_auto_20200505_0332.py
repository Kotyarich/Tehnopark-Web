# Generated by Django 3.0.5 on 2020-05-05 03:32

import django.contrib.postgres.indexes
import django.contrib.postgres.search
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0007_create_search_triggers'),
    ]

    operations = [
        migrations.CreateModel(
            name='PgQuestionSearch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search_vector_title', django.contrib.postgres.search.SearchVectorField(null=True)),
                ('search_vector_text', django.contrib.postgres.search.SearchVectorField(null=True)),
                ('question', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='pg_question', to='questions.Question')),
            ],
            options={
                'required_db_vendor': 'postgresql',
            },
        ),
        migrations.AddIndex(
            model_name='pgquestionsearch',
            index=django.contrib.postgres.indexes.GinIndex(fields=['search_vector_title', 'search_vector_text'], name='questions_p_search__8a62bd_gin'),
        ),
    ]
