from .models import User


class EmailBackend(object):
    def authenticate(self, username, password):
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            pass
        else:
            if user.check_password(password):
                return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
