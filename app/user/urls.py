from django.urls import path
from .views import UserCreateAPIView, CreateTokenView

app_name = 'user'

urlpatterns = [
    path('create/', UserCreateAPIView.as_view(), name='create'),
    path('token/', CreateTokenView.as_view(), name='token'),
]
