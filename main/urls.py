from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.MainPageView.as_view(), name='index'),
]
