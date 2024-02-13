from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.http import JsonResponse
from .utils import DataMixin
from .models import *
from .forms import *
import requests

class Index(DataMixin, TemplateView):
    template_name='main/index.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        c_def = self.get_data(title = 'Homepage')
        return context | c_def
    
    def get(self, request, *args, **kwargs):
        url = 'http://127.0.0.1:8000/api/'

        context = self.get_context_data(**kwargs)
        y = context['y']
        m = context['m']

        data = {
            'y': y,
            'm': m,
        }

        response = requests.get(url, params=data)

        if response.status_code == 200:
            days = response.json().get('days')
            context['year_month'] = response.json().get('title')
            for week in days:
                for day in week:
                    if day.get('number') == context['d']:
                        context['today'] = day
                        break

        return self.render_to_response(context)
    
class Month(DataMixin, TemplateView):
    template_name = 'main/month.html'

    def get(self, request, *args, **kwargs):
        url = 'http://127.0.0.1:8000/api/'

        context = self.get_context_data(**kwargs)
        y = kwargs['y']
        m = kwargs['m']

        data = {
            'y': y,
            'm': m,
        }

        response = requests.get(url, params=data)

        if response.status_code == 200:
            context['api_data'] = response.json()
            context['title'] = response.json().get('title')
        
        return self.render_to_response(context)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        c_def = self.get_data(title = 'title')
        return context | c_def