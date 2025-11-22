from django.core.exceptions import ValidationError
from django.db import models

from config.settings import AUTH_USER_MODEL


class Habit(models.Model):
    """Модель привычки"""

    action = models.CharField(max_length=200, verbose_name='действие')
    user = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='habits', blank=True, verbose_name='пользователь'
    )
    place = models.CharField(max_length=100, blank=True, null=True, verbose_name='место')
    periodicity: int = models.PositiveIntegerField(
        default=1, blank=True, null=True, verbose_name='периодичность в неделю'
    )
    start_time = models.TimeField(blank=True, null=True, verbose_name='время')
    execution_time: int = models.PositiveIntegerField(
        default=120, blank=True, null=True, verbose_name='время выполнения (секунды)'
    )
    is_pleasant = models.BooleanField(default=False, verbose_name='признак приятной привычки')
    related_habit = models.ForeignKey(
        'self', on_delete=models.SET_NULL, blank=True, null=True, verbose_name='связанная привычка'
    )
    reward = models.CharField(max_length=200, blank=True, null=True, verbose_name='вознаграждение')
    is_published = models.BooleanField(default=False, verbose_name='публичность')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    is_reminder_send = models.BooleanField(default=False, blank=True, null=True, verbose_name='Напоминание отправлено')
    update_reminder_send_flag = models.DateField(blank=True, null=True, verbose_name='Дата отправки напоминания')

    class Meta:
        verbose_name = 'привычка'
        verbose_name_plural = 'привычки'
        ordering = ['user', '-created_at']
        db_table = 'habits'

    def __str__(self):
        return f'Привычка {self.action}'

    def clean(self):
        """Валидация на уровне модели"""
        errors = {}

        # Приятная привычка
        if self.is_pleasant:
            if self.related_habit:
                errors['related_habit'] = 'Приятная привычка не может иметь связанную привычку'
            if self.reward:
                errors['reward'] = 'Приятная привычка не может иметь вознаграждение'

        # Полезная привычка
        else:
            if self.related_habit and self.reward:
                errors['reward'] = 'Можно указать только вознаграждение ИЛИ связанную привычку'
                errors['related_habit'] = 'Можно указать только вознаграждение ИЛИ связанную привычку'

            if not self.start_time:
                errors['start_time'] = 'Для полезной привычки должно быть указано время начала'

            if not self.reward and not self.related_habit:
                errors['reward'] = 'Укажите вознаграждение или связанную привычку'

            if self.related_habit and not self.related_habit.is_pleasant:
                errors['related_habit'] = 'Связанная привычка должна быть приятной'

            if self.execution_time > 120:
                errors['execution_time'] = 'Время выполнения не должно превышать 120 секунд'

            if self.periodicity > 7:
                errors['periodicity'] = 'Периодичность не должна превышать 7 дней'

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
