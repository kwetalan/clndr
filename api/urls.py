from django.urls import path
from .views import *

app_name = 'api'

urlpatterns = [
    path('', APIData.as_view(), name='api'),
]