from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, FormView, View
from django.views.generic.detail import SingleObjectMixin
from .models import Article as A, Profile
from .forms import *
from main.utils import DataMixin
from django.db.models import F
from django.template.defaultfilters import slugify
from django.contrib.auth.mixins import LoginRequiredMixin

class Blog(DataMixin, ListView):
    model = A
    template_name = 'blog/blog.html'

    def get_context_data(self, **kwargs):
        queryset = self.get_queryset()
        articles_by_views = queryset.order_by('-date')
        articles_by_time = queryset
        context = super().get_context_data(**kwargs)
        c_def = self.get_data(title = 'Blog', articles_by_views = articles_by_views, articles_by_time = articles_by_time)
        return context | c_def

class Article(DataMixin, DetailView):
    model = A
    template_name = 'blog/article.html'
    context_object_name = 'article'

    def get(self, request, *args, **kwargs):
        article = self.get_object()
        article.views = F('views') + 1
        article.save()
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_data(title = context['article'].header)
        return context | c_def
    
class ArticleDetail(View):
    def get(self, request, *args, **kwargs):
        view = ArticleDisplay.as_view()
        return view(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        view = ArticleComment.as_view()
        return view(request, *args, **kwargs)

class ArticleDisplay(DataMixin, DetailView):
    model = A
    template_name = 'blog/article.html'
    context_object_name = 'article'

    def get(self, request, *args, **kwargs):
        article = self.get_object()
        article.views = F('views') + 1
        article.save()
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment_list = Comment.objects.filter(article_id = context['article']).order_by('-date')
        form = AddCommentForm()
        c_def = self.get_data(comment_list = comment_list, form = form)
        return c_def | context

    # model = Article
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     title = context['article'].title
    #     comment_list = Comment.objects.filter(article = context['article']).order_by('-date')
    #     category_list = context['article'].category.all()
    #     form = AddCommentForm()
    #     c_def = self.get_data(title = title, comment_list = comment_list,
    #                            category_list = category_list, form = form)
    #       return c_def | context
    
class ArticleComment(SingleObjectMixin, FormView):
    model = A
    form_class = AddCommentForm
    template_name = 'blog/article.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)
    
    def get_form_kwargs(self):
        kwargs = super(ArticleComment, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    
    def form_valid(self, form):
        comment = form.save(commit = False)
        post = self.get_object()
        comment.post = self.object
        comment.article_id = A.objects.get(slug = post.slug)
        comment.author_id = Profile.objects.get(user = self.request.user) 
        comment.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        post = self.get_object()
        return reverse('blog:article', kwargs = {'slug': post.slug})

class AddArticle(LoginRequiredMixin, DataMixin, CreateView):
    model = A
    form_class = AddArticleForm
    template_name = 'blog/add_article.html'
    success_url = reverse_lazy('blog:blog')

    def get_unique_slug(self, fields):
        slug = slugify(fields.header)
        slug_number = 0
        sorted_articles = A.objects.filter(slug__contains = slug)
        for article in sorted_articles:
            try:
                if article.slug == slug + '-' + article.slug[len(slug) + 1] or article.slug == slug:
                    slug_number += 1
                    
            except IndexError:
                if article.slug == slug:
                    slug_number += 1
        return slug + '-' + str(slug_number) if slug_number > 0 else slug

    def form_valid(self, form):
        article = form.save(commit = False)
        article.author_id = self.request.user
        article.slug = self.get_unique_slug(article)
        article.save()
        return super().form_valid(form)
        
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_data(title = 'Add Article')
        return context | c_def
