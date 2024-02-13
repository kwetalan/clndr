from collections.abc import Iterable
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='s_user')
    slug = models.SlugField(null=True, blank=True)
    avatar = models.ImageField(
        verbose_name='Аватар',
        upload_to='images/avatars/%Y/%m/%d/',
        default='images/avatars/default.jpg',
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'jpeg'))])
    bio = models.TextField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    coordinates = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.slug
    
    def get_absolute_url(self):
        return f'accounts/profile/{self.slug}'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'