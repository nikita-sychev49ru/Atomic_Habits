from celery import shared_task
from celery.apps.worker import logger

from i_can.models import Habit
from i_can.services import send_telegram_message
from users.models import User


@shared_task
def send_reminder_to_telegram():
    """Отправка напоминания в Телеграм о привычке"""
    from django.utils import timezone

    # Используем timezone-aware datetime
    now = timezone.now()
    current_time = now.time()
    current_date = now.date()

    logger.info(f"Задача запущена в: {now}")
    logger.info(f"Текущее время сервера (МСК): {current_time}")
    logger.info(f"Текущая дата: {current_date}")

    users = User.objects.filter(tg_id__isnull=False)

    for user in users:
        habits = Habit.objects.filter(user=user, start_time__isnull=False, is_reminder_send=False)

        for habit in habits:
            if habit.periodicity == 0:
                continue

            # Проверяем день недели (0-понедельник, 6-воскресенье)
            current_weekday = now.weekday()
            logger.info(
                f"Текущий день недели: {current_weekday}, привычка: {habit.action}, периодичность: {habit.periodicity}"
            )

            # Проверяем, нужно ли выполнять привычку сегодня
            if current_weekday % habit.periodicity != 0:
                logger.info(f"Пропускаем привычку {habit.action} - не подходит по периодичности")
                continue

            # Проверяем, наступило ли время для привычки
            logger.info(f"Сравниваем время: привычка {habit.start_time} <= текущее {current_time}")
            if habit.start_time <= current_time:
                message = f'''Напоминание о привычке:\n{habit.action}\nМесто: {habit.place or "не указано"}\n
                Время выполнения: {habit.execution_time} секунд'''

                try:
                    send_telegram_message(user.tg_id, message)
                    habit.is_reminder_send = True
                    habit.update_reminder_send_flag = current_date
                    habit.save()
                    logger.info(f'Отправлено напоминание пользователю {user.email} для привычки {habit.action}')
                except Exception as e:
                    logger.error(f'Ошибка отправки пользователю {user.email}: {e}')


@shared_task(bind=True)
def reset_reminder_flags(self):
    """Сброс флагов напоминаний на основе периодичности"""
    from django.utils import timezone

    now = timezone.now()
    logger.info(f'=== Задача reset_reminder_flags запущена в {now} (МСК) ===')

    try:
        habits_with_reminders = Habit.objects.filter(is_reminder_send=True, update_reminder_send_flag__isnull=False)

        updated_count = 0
        current_date = now.date()

        for habit in habits_with_reminders:
            if habit.update_reminder_send_flag:
                days_passed = (current_date - habit.update_reminder_send_flag).days
                logger.info(f"Привычка {habit.action}: дней прошло {days_passed}, периодичность {habit.periodicity}")

                if days_passed >= habit.periodicity:
                    habit.is_reminder_send = False
                    habit.save()
                    updated_count += 1
                    logger.info(f'Сброшен флаг для привычки {habit.id}')

        logger.info(f'Обновлено записей: {updated_count}')
        return updated_count

    except Exception as e:
        logger.error(f'Ошибка в reset_reminder_flags: {e}')
        raise
