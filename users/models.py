from django.db import models
from django.utils import timezone



class Owner(models.Model):
    username = models.CharField(max_length = 50)
    email = models.EmailField()
    password = models.CharField(max_length = 100)
    is_active = models.BooleanField(default = True)


class Galleries(models.Model):
    user = models.ForeignKey(Owner, on_delete = models.CASCADE)
    name = models.CharField(max_length = 50, unique=True)
    slug = models.SlugField(max_length = 50, unique=True)
    password = models.CharField(max_length = 20)
    description = models.TextField(max_length = 100, null = True, blank = True)
    created_date = models.DateTimeField(default = timezone.datetime.now)
    is_active = models.BooleanField(default = True)

    class Meta:
        verbose_name = 'gallery'
        verbose_name_plural = 'galleries'