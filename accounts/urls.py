from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserRegisterView.as_view(), name='signup'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/<slug:slug>', ProfileDetailView.as_view(), name='profile'),
    path('edit/', ProfileUpdateView.as_view(), name='edit'),
]