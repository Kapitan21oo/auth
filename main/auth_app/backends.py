from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q


class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(Q(email=email))
        except UserModel.DoesNotExist:
            print(f"Пользователь с электронной почтой '{email}' не найден")
            return None

        if user.check_password(password):
            print(f"Пользователь '{email}' успешно аутентифицирован")
            return user
        else:
            print(f"Неверный пароль для пользователя '{email}'")
            return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
