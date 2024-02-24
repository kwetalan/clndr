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
import asyncio
import aiohttp

class Index(DataMixin, TemplateView):
    template_name='main/index.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        c_def = self.get_data(title = 'Homepage')
        return context | c_def
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        y = context['y']
        m = context['m']

        url = f'http://127.0.0.1:8000/api/?y={y}&m={m}'

        async def fetch_data(url):
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    data = await response.json()
                    return data

        async def main():
            api_data = await fetch_data(url)
            days = api_data.get('days')
            context['year_month'] = api_data.get('title')
            for week in days:
                for day in week:
                    if day.get('number') == context['d']:
                        context['today'] = day
                        break

        asyncio.run(main()) 

        return self.render_to_response(context)
    
class Month(DataMixin, TemplateView):
    template_name = 'main/month.html'

    def get(self, request, *args, **kwargs):
        
        context = self.get_context_data(**kwargs)
        y = kwargs['y']
        m = kwargs['m']

        url = f'http://127.0.0.1:8000/api/?y={y}&m={m}'

        async def fetch_data(url):
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    data = await response.json()
                    return data

        async def main():
            context['api_data'] = await fetch_data(url)
            context['title'] = context['api_data'].get('title')

        asyncio.run(main()) 
        
        return self.render_to_response(context)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        c_def = self.get_data(title = 'title')
        return context | c_def