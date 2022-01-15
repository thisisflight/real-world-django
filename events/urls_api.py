from django.urls import path
from .views import create_review

app_name = 'api_events'

urlpatterns = [
    path('reviews/create/', create_review, name='create_review'),
]
