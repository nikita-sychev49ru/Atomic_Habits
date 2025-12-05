from rest_framework.serializers import ValidationError


class HabitFieldsValidator:
    """Валидатор значений полей объекта Habit"""

    def __call__(self, attrs, instance=None):
        """Основная валидация"""
        # Получаем текущие значения из атрибутов для обновления привычки
        if instance:
            is_pleasant = attrs.get('is_pleasant', instance.is_pleasant)
            related_habit = attrs.get('related_habit', instance.related_habit)
            reward = attrs.get('reward', instance.reward)
            periodicity = attrs.get('periodicity', instance.periodicity)
            start_time = attrs.get('start_time', instance.start_time)
            execution_time = attrs.get('execution_time', instance.execution_time)
        else:
            # Для создания новой привычки
            is_pleasant = attrs.get('is_pleasant', False)
            related_habit = attrs.get('related_habit')
            reward = attrs.get('reward')
            periodicity = attrs.get('periodicity', 7)
            start_time = attrs.get('start_time')
            execution_time = attrs.get('execution_time', 120)

        # Проверка времени выполнения
        if 'execution_time' in attrs and execution_time > 120:
            raise ValidationError({'execution_time': 'Время исполнения не должно превышать 120 секунд'})

        # Проверка периодичности
        if 'periodicity' in attrs and periodicity and periodicity > 7:
            raise ValidationError({'periodicity': 'Привычка должна выполняться не реже 1 раза в 7 дней'})

        # Валидация для приятных привычек
        if is_pleasant:
            if 'related_habit' in attrs and related_habit:
                raise ValidationError({'related_habit': 'Приятная привычка не может иметь связанную привычку'})
            if 'reward' in attrs and reward:
                raise ValidationError({'reward': 'Приятная привычка не может иметь вознаграждение'})

        # Валидация для полезных привычек
        else:
            # Нельзя одновременно иметь и вознаграждение и связанную привычку
            if ('related_habit' in attrs or 'reward' in attrs) and related_habit and reward:
                raise ValidationError(
                    {
                        'reward': 'Можно указать только вознаграждение ИЛИ связанную привычку',
                        'related_habit': 'Можно указать только вознаграждение ИЛИ связанную привычку',
                    }
                )

            # Должны быть заполнены обязательные поля
            if 'start_time' in attrs and not start_time:
                raise ValidationError({'start_time': 'Для полезной привычки должно быть указано время начала'})

            # Должно быть либо вознаграждение, либо связанная привычка
            if ('reward' in attrs and not reward and not related_habit) or (
                'related_habit' in attrs and not related_habit and not reward
            ):
                raise ValidationError(
                    {
                        'reward': 'Для полезной привычки укажите вознаграждение ИЛИ связанную привычку',
                        'related_habit': 'Для полезной привычки укажите вознаграждение ИЛИ связанную привычку',
                    }
                )

            # Если указана связанная привычка, она должна быть приятной
            if 'related_habit' in attrs and related_habit and not related_habit.is_pleasant:
                raise ValidationError({'related_habit': 'Связанная привычка должна быть приятной'})
