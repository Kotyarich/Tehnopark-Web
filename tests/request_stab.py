class SessionStab:
    def flush(self):
        pass


class RequestStab:
    def __init__(self, user):
        self.user = user
        self.session = SessionStab()
