from django.db import models
from users.models import Galleries

class Category(models.Model):
    gallery_id = models.ForeignKey(Galleries, on_delete = models.CASCADE)
    name = models.CharField(max_length=100)


    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

class Photo(models.Model):
    gallery_id = models.ForeignKey(Galleries, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL) #カテゴリが消えてもOK
    image = models.ImageField(null=False, blank=False)
    title = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)
    created_date = models.DateTimeField(auto_now = True)

    # def __str__(self):
    #     return self.description