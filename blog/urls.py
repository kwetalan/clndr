from django.urls import path
from .views import *

app_name = 'blog'

urlpatterns = [
    path('', Blog.as_view(), name='blog'),
    path('add_article/', AddArticle.as_view(), name='add_article'),
    path('<slug:slug>/', ArticleDetail.as_view(), name='article'),
]