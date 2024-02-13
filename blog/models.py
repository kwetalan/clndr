from django.db import models
from django.contrib.auth.models import User
from accounts.models import Profile

class Article(models.Model):
    header = models.CharField(max_length=255)
    content = models.TextField()
    author_id = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField()
    date = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default = 0)

    def __str__(self):
        return self.header
    
    def get_absolute_url(self):
        return f'/{self.slug}'
    
    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Comment(models.Model):
    content = models.TextField()
    author_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    article_id = models.ForeignKey('Article', on_delete=models.CASCADE, null=True)
    comment_id = models.ForeignKey('Comment', on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f'Comment by {self.author_id} on {self.date}'
    
    class Meta:
        verbose_name = 'Комент'
        verbose_name_plural = 'Коменты'