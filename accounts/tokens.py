from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()


class EmailOrUsernameTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Accepts: { "login": "email OR username", "password": "..." }
    """

    def validate(self, attrs):
        login = attrs.get("login")
        password = attrs.get("password")

        if not login:
            raise AuthenticationFailed({"login": ["This field is required."]})
        if not password:
            raise AuthenticationFailed({"password": ["This field is required."]})

        try:
            if "@" in login:
                user = User.objects.get(email__iexact=login)
            else:
                user = User.objects.get(username__iexact=login)
        except User.DoesNotExist:
            raise AuthenticationFailed("No active account found with the given credentials")

        # feed SimpleJWT what it expects
        attrs["username"] = user.username
        attrs["password"] = password
        attrs.pop("login", None)

        return super().validate(attrs)

