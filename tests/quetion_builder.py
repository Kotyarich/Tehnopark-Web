from questions.models import Question, PgQuestionSearch


class QuestionBuilder:

    def __init__(self, author):
        self.question = Question.objects.create(author=author)

    def add_tag(self, tag):
        self.question.tags.add(tag)
        return self

    def with_rating(self, rating):
        self.question.rating = rating
        return self

    def with_text(self, text):
        self.question.text = text
        return self

    def with_title(self, title):
        self.question.title = title
        return self

    def with_data(self, data):
        self.question.created_at = data
        return self

    def with_pg_search(self):
        PgQuestionSearch.objects.create(question=self.question,
                                        search_vector_title=self.question.title,
                                        search_vector_text=self.question.text)
        return self

    def build(self):
        return self.question
