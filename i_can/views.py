from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from i_can.models import Habit
from i_can.pagination import HabitPagination
from i_can.permissions import IsOwner
from i_can.serializers import HabitSerializer, PublicHabitSerializer


class HabitCreateAPIView(generics.CreateAPIView):
    """Контроллер создания привычки"""

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()

    def perform_create(self, serializer):
        """Запись пользователя в качестве автора привычки"""
        serializer.save(user=self.request.user)


class HabitListAPIView(generics.ListAPIView):
    """Контроллер получения списка всех своих привычек"""

    serializer_class = HabitSerializer
    pagination_class = HabitPagination

    filter_backends = [DjangoFilterBackend]
    filterset_fields = (
        'is_pleasant',
        'periodicity',
        'is_published',
    )

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)


class PublicHabitListAPIView(generics.ListAPIView):
    serializer_class = PublicHabitSerializer
    pagination_class = HabitPagination

    filter_backends = [DjangoFilterBackend]
    filterset_fields = (
        'user',
        'action',
        'is_pleasant',
    )

    def get_queryset(self):
        return Habit.objects.filter(is_published=True)


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    """Контроллер просмотра одной привычки"""

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = (IsOwner,)


class HabitUpdateAPIView(generics.UpdateAPIView):
    """Контроллер изменения одной привычки"""

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = (IsOwner,)


class HabitDestroyAPIView(generics.DestroyAPIView):
    """Контроллер удаления одной привычки"""

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = (IsOwner,)
