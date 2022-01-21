from django.urls import path
from django.views.decorators.http import require_POST

from .views import (EventListView, EventDetailView, EnrollToEventView,
                    EventCreateView, EventUpdateView, EventDeleteView)

app_name = 'events'

urlpatterns = [
    path('list/', EventListView.as_view(), name='event_list'),
    path('detail/<int:pk>/', EventDetailView.as_view(), name='event_detail'),
    path('event-enroll/', require_POST(EnrollToEventView.as_view()), name='event_enroll'),
    path('create-event/', EventCreateView.as_view(), name='event_create'),
    path('update-event/<int:pk>/', EventUpdateView.as_view(), name='event_update'),
    path('delete-event/<int:pk>/', require_POST(EventDeleteView.as_view()), name='event_delete'),
]
