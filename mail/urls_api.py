from django.urls import path
from . import api


app_name = 'api_mail'

urlpatterns = [
    path('create-letters/', api.create_letters_view, name='create_letters'),
    path('get_subscribers/', api.get_subscribers, name='get_subscribers'),
    path('send_letters/', api.send_letters_view, name='send_letters')
]
