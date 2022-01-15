from django.urls import path
from .views import get_event_detail, get_event_list

app_name = 'events'

urlpatterns = [
    path('list/', get_event_list, name='event_list'),
    path('detail/<int:pk>/', get_event_detail, name='event_detail'),
]
