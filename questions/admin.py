from django.contrib import admin
from django.db.models import Count, DateTimeField, Max
from django.db.models.functions import Trunc

from .models import Tag, Question, Answer


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    change_list_template = 'admin/tag_change_list.html'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        metrics = {
            'questions': Count('questions__id', distinct=True),
            'answers': Count('questions__question', distinct=True),
        }

        response.context_data['summary'] = list(
            qs.values('text').annotate(**metrics).order_by('-questions')
        )
        response.context_data['summary_total'] = dict(
            qs.aggregate(**metrics)
        )

        return response


def get_next_in_date_hierarchy(request, date_hierarchy):
    if date_hierarchy + '__day' in request.GET:
        return 'hour'
    if date_hierarchy + '__month' in request.GET:
        return 'day'
    if date_hierarchy + '__year' in request.GET:
        return 'week'
    return 'month'


class AdminTimeGraph(admin.ModelAdmin):
    date_hierarchy = 'created_at'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        period = get_next_in_date_hierarchy(request, self.date_hierarchy)
        response.context_data['period'] = period

        summery_over_time = qs.annotate(
            period=Trunc(
                'created_at', period, output_field=DateTimeField()
            ),
        ).values('period') \
            .annotate(total=Count('id')) \
            .order_by('period')

        summary_range = summery_over_time.aggregate(high=Max('total'))
        high = summary_range.get('high', 0)

        response.context_data['summary_over_time'] = [{
            'period': x['period'],
            'total': x['total'] or 0,
            'pct': (x['total'] or 0) / high * 100,
        } for x in summery_over_time]

        return response


@admin.register(Question)
class QuestionAdmin(AdminTimeGraph):
    change_list_template = 'admin/question_change_list.html'


@admin.register(Answer)
class AnswerAdmin(AdminTimeGraph):
    change_list_template = 'admin/answer_change_list.html'
