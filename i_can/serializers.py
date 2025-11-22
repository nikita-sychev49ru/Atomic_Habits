from rest_framework import serializers

from i_can.models import Habit
from i_can.validators import HabitFieldsValidator


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор для объектов привычек"""

    class Meta:
        model = Habit
        fields = '__all__'

        extra_kwargs = {
            'user': {'read_only': True},
            'created_at': {'read_only': True},
        }

    def validate(self, attrs):
        """Валидация на уровне сериализатора"""
        validator = HabitFieldsValidator()
        validator(attrs, self.instance)
        return attrs


class PublicHabitSerializer(serializers.ModelSerializer):
    """Сериализатор для публичных привычек"""

    class Meta:
        model = Habit
        fields = ("action", "is_pleasant", "execution_time")
