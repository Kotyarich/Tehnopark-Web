import logging

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from channels.layers import get_channel_layer

from questions.models import Profile

logger = logging.getLogger(__name__)


class NotificationConsumer(JsonWebsocketConsumer):
    def connect(self):
        """
        Called when the websocket is handshaking as part of initial connection.
        """
        try:
            if not self.scope['user'].is_authenticated:
                logger.error('User in not authenticated')
                self.close()

            user = Profile.objects.get_authenticated(self.scope['user'])
            group_name = user.group_name

            async_to_sync(self.channel_layer.group_add)(
                group_name,
                self.channel_name,
            )

            self.accept()
        except Exception as e:
            logger.error(e)
            self.close()

    def liked(self, event):
        self.send_json(
            {
                "user": event["user"],
                "value": event["value"],
                "question": event["question"],
            },
        )

    def disconnect(self, code):
        """
        Called when the websocket closes for any reason.
        Leave all the rooms we are still in.
        """
        try:
            if not self.scope['user'].is_authenticated:
                logger.error('User in not authenticated')
                self.close()

            user = Profile.objects.get(user=self.scope['user'])
            group_name = user.group_name

            self.channel_layer.group_discard(group_name, self.channel_name)
        except Exception as e:
            logger.error(e)


class NotificationSender:
    _event_type = 'liked'

    @classmethod
    def notify_question_liked(cls, user, value, question):
        profile = user.user

        async_to_sync(get_channel_layer().group_send)(profile.group_name, {
            'type': cls._event_type,
            'user': profile.nickname,
            'value': value,
            'question': question.title
        })
