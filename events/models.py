from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.db import models
from django.urls import reverse

EVENT_SOLD_OUT = '0 (sold-out)'
EVENT_SOLD_LESS_OR_EQUAL_THAN_50_PERCENT = '(<= 50%)'
EVENT_SOLD_GREATER_THAN_50_PERCENT = '(> 50%)'


class Event(models.Model):
    title = models.CharField(
        max_length=200,
        default='',
        verbose_name='Название')
    logo = models.ImageField(upload_to='events', verbose_name='Лого события',
                             null=True, blank=True)
    description = models.TextField(default='', verbose_name='Описание')
    date_start = models.DateTimeField(verbose_name='Дата начала')
    participants_number = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(10000)],
        verbose_name='Количество участников')
    is_private = models.BooleanField(default=False, verbose_name='Частное')
    category = models.ForeignKey('Category', on_delete=models.CASCADE,
                                 related_name='events',
                                 verbose_name='Категория')
    features = models.ManyToManyField('Feature', verbose_name='Свойства событий')

    class Meta:
        db_table = 'events'
        verbose_name = 'Событие'
        verbose_name_plural = 'События'

    def __str__(self):
        return self.title

    def display_enroll_count(self):
        return self.enrolls.count()

    display_enroll_count.short_description = 'Количество записей'

    def display_places_left(self):
        signed_participants = self.display_enroll_count()
        if not (self.participants_number - signed_participants):
            return EVENT_SOLD_OUT
        elif self.participants_number / 2 >= signed_participants:
            return f"{self.participants_number - signed_participants} {EVENT_SOLD_LESS_OR_EQUAL_THAN_50_PERCENT}"
        elif 0 < self.participants_number / 2 < signed_participants:
            return f"{self.participants_number - signed_participants} {EVENT_SOLD_GREATER_THAN_50_PERCENT}"

    display_places_left.short_description = 'Осталось мест'

    @property
    def rate(self):
        return (round(sum(review.rate for review in self.reviews.all()) / self.reviews.count(), 1)
                if self.reviews.count() else 0)

    @property
    def logo_url(self):
        return self.logo.url if self.logo else f"{settings.STATIC_URL}images/svg-icon/event.svg"

    @property
    def places_left(self):
        return self.participants_number - self.display_enroll_count()

    def get_absolute_url(self):
        return reverse('events:event_detail', args=[str(self.pk)])

    def get_update_url(self):
        return reverse('events:event_update', args=[str(self.pk)])

    def get_delete_url(self):
        return reverse('events:event_delete', args=[str(self.pk)])


class Category(models.Model):
    title = models.CharField(
        max_length=90,
        default='',
        verbose_name='Категория')

    class Meta:
        db_table = 'categories'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def display_event_count(self):
        return self.events.count()

    def __str__(self):
        return self.title


class Feature(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Название'
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'features'
        verbose_name = 'Свойство события'
        verbose_name_plural = 'Свойства событий'


class Enroll(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Пользователь',
                             related_name='enrolls')
    event = models.ForeignKey(Event, on_delete=models.CASCADE,
                              verbose_name='События',
                              related_name='enrolls')
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Создано')

    def __str__(self):
        return self.event.title

    class Meta:
        db_table = 'enrolls'
        verbose_name = 'Запись на событие'
        verbose_name_plural = 'Записи на события'


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Пользователь',
                             related_name='reviews')
    event = models.ForeignKey(Event, on_delete=models.CASCADE,
                              verbose_name='События',
                              related_name='reviews')
    rate = models.PositiveSmallIntegerField(verbose_name='Оценка пользователя')
    text = models.TextField(verbose_name='Текст отзыва')
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Создано')
    updated = models.DateTimeField(auto_now=True,
                                   verbose_name='Изменено')

    def __str__(self):
        return self.event.title

    class Meta:
        db_table = 'reviews'
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
