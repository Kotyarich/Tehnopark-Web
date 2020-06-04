from questions.models import Like, Profile, Question, Answer
from .consumers import NotificationSender


class LikeQuestion:
    def __init__(self, user, value, question_id):
        self._user = user
        self._value = value
        self._question_id = question_id

    def run_use_case(self):
        profile = Profile.objects.get_authenticated(self._user)
        question = Question.objects.get(id=self._question_id)
        old_rating = question.rating

        self._create_like(profile, question)
        if question.rating != old_rating:
            self._send_notification(question)

        return {'rating': question.rating}

    def _send_notification(self, question):
        NotificationSender.notify_question_liked(
            self._user,
            self._value,
            question
        )

    def _create_like(self, profile, question):
        return Like.objects.like(profile, self._value, question)


class LikeAnswer:
    def __init__(self, user, value, question_id):
        self._user = user
        self._value = value
        self._question_id = question_id

    def run_use_case(self):
        profile = Profile.objects.get_authenticated(self._user)
        answer = Answer.objects.get(id=self._question_id)

        self._create_like(profile, answer)

        return {'rating': answer.rating}

    def _create_like(self, profile, answer):
        return Like.objects.like(profile, self._value, answer)
