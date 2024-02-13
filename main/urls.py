from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', Index.as_view(), name='home'),
    path('month/<int:y>/<int:m>', Month.as_view(), name='month'),
]
