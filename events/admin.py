from django.contrib import admin

from .models import (Category, Feature,
                     Enroll, Event, Review,
                     EVENT_SOLD_OUT,
                     EVENT_SOLD_GREATER_THAN_50_PERCENT,
                     EVENT_SOLD_LESS_OR_EQUAL_THAN_50_PERCENT)


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    can_delete = False
    readonly_fields = [field.name for field in Review._meta.fields
                       if field.name != 'id']

    def has_add_permission(self, request, obj):
        return False


class EventSoldFilter(admin.SimpleListFilter):
    title = 'Заполненность'
    parameter_name = 'event_sold_filter'

    def lookups(self, request, model_admin):
        filter_list = (
            ('0', EVENT_SOLD_OUT),
            ('1', EVENT_SOLD_LESS_OR_EQUAL_THAN_50_PERCENT),
            ('2', EVENT_SOLD_GREATER_THAN_50_PERCENT)
        )
        return filter_list

    def queryset(self, request, queryset):
        filter_value = self.value()
        if filter_value == '0':
            sold_out_events_ids = [event.id for event in queryset if
                                   event.display_places_left() == EVENT_SOLD_OUT]
            return queryset.filter(id__in=sold_out_events_ids)
        elif filter_value == '1':
            sold_less_or_equal_ids = [event.id for event in queryset if
                                      event.participants_number / 2 >= event.display_enroll_count()]
            return queryset.filter(id__in=sold_less_or_equal_ids)
        elif filter_value == '2':
            sold_greater_than_ids = [event.id for event in queryset if
                                     event.participants_number / 2 < event.display_enroll_count()
                                     and event.participants_number - event.display_enroll_count()]
            return queryset.filter(id__in=sold_greater_than_ids)
        return queryset


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'display_event_count']
    list_display_links = ['id', 'title']


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    list_display_links = ['id', 'title']


@admin.register(Enroll)
class EnrollAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'event', 'created']
    list_select_related = ['user', 'event']
    list_display_links = ['id', 'user', 'event']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'date_start',
                    'is_private', 'category', 'participants_number',
                    'display_enroll_count', 'display_places_left']
    list_select_related = ['category']
    ordering = ['date_start']
    search_fields = ['title']
    fields = ([field.name for field in Event._meta.fields if field.name != 'id'] +
              ['display_enroll_count', 'display_places_left', 'features'])
    readonly_fields = ['display_enroll_count', 'display_places_left']
    filter_horizontal = ['features']
    list_filter = [EventSoldFilter, 'category', 'features']
    inlines = [ReviewInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'event', 'created']
    list_display_links = ['id', 'user', 'event']
    list_select_related = ['user', 'event']
    list_filter = ['event', 'created']
    fields = ['id', 'created', 'updated']
    readonly_fields = ['created', 'updated', 'id', ]
