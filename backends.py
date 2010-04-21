from signup.models import CustomUser
from django.contrib.auth.backends import ModelBackend

class NoAuthBackend(ModelBackend):
    """
    Authenticates against signup.models.CustomUser, without requiring
    authorisation
    """
    def authenticate(self, username=None, password=None):
        try:
            user = CustomUser.objects.get(username=username)
            user.login_count += 1
            user.save()
            return user
        except CustomUser.DoesNotExist:
            try:
                user = CustomUser.objects.get(email=username)
                user.login_count += 1
                user.save()
                return user
            except:
                return None

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None

