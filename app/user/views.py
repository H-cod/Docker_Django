from rest_framework.generics import CreateAPIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from .serializers import UserCreateSerializer, AuthTokenSerializer


class UserCreateAPIView(CreateAPIView):
    """Create new user in the system"""
    serializer_class = UserCreateSerializer


class CreateTokenView(ObtainAuthToken):
    """Create new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
