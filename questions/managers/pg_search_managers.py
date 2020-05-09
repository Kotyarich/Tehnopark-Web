from django.contrib.postgres.search import SearchRank
from django.db.models import Manager


class PgSearchQuestionManager(Manager):
    def most_similar(self, search_vector, query):
        rank = SearchRank(search_vector, query)
        ranked_result = self.annotate(rank=rank).order_by('-rank')
        return ranked_result.select_related('question')
