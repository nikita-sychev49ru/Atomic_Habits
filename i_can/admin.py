from django.contrib import admin

from .models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = (
        'action',
        'user',
        'place',
        'periodicity',
        'start_time',
        'execution_time',
        'is_pleasant',
        'related_habit',
        'reward',
        'is_published',
        'created_at',
        'is_reminder_send',
    )
    list_filter = ('user',)
