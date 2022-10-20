from django.contrib import admin

from .models import Photo, Category

# class PhotoAdmin(admin.ModelAdmin):
#     list_display = ('title', 'category', 'created_date')
#     list_filter = ('category',)

admin.site.register(Category)
admin.site.register(Photo)
