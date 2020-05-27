from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer

from questions.models import Profile


class NotificationConsumer(JsonWebsocketConsumer):
    def connect(self):
        """
        Called when the websocket is handshaking as part of initial connection.
        """
        try:
            if not self.scope['user'].is_authenticated:
                # TODO logger.error('User in not authenticated')
                self.close()

            user = Profile.objects.get_authenticated(self.scope['user'])
            group_name = user.group_name

            async_to_sync(self.channel_layer.group_add)(
                group_name,
                self.channel_name,
            )

            self.accept()
        except Exception as e:
            # TODO logger.error(e)
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
            if not self.scope['user'].is_aunthenticated:
                # TODO logger.error('User in not authenticated')
                self.close()

            user = Profile.objects.get(user=self.scope['user'])
            group_name = user.group_name

            self.channel_layer.group_discard(group_name, self.channel_name)
        except Exception as e:
            # TODO logger.error(e)
            pass
