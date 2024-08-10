# anonymous_user.py

from flask_login import AnonymousUserMixin

class AnonymousUser(AnonymousUserMixin):
    @property
    def is_authenticated(self):
        return False

    @property
    def is_active(self):
        return False

    @property
    def is_anonymous(self):
        return True

    def get_id(self):
        return None
