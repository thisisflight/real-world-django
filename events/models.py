from django.core.validators import MaxValueValidator
from django.db import models


class Event(models.Model):
    title = models.CharField(
        max_length=200,
        default='',
        verbose_name='Название')
    description = models.TextField(default='', verbose_name='Описание')
    date_start = models.DateTimeField(verbose_name='Дата начала')
    participants_number = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(10000)],
        verbose_name='Количество участников')
    is_private = models.BooleanField(default=False, verbose_name='Частное')

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(
        max_length=90,
        default='',
        verbose_name='Категория')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title
