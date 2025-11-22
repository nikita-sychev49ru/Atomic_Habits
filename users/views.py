from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import User
from users.serializers import UserRegistrationSerializer, UserSerializer


class UserRegistrationAPIView(generics.CreateAPIView):
    """контроллер для регистрации пользователя"""

    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]


class UserViewSet(viewsets.ModelViewSet):
    """вьюсет представлений для объектов модели пользователя"""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
