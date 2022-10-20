from django.contrib import admin

from .models import Owner, Galleries

class OwnersAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_active')

class GalleriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    list_display = ('name', 'description', 'is_active')
    readonly_fields = ('password', 'created_date')

admin.site.register(Owner, OwnersAdmin)
admin.site.register(Galleries, GalleriesAdmin)


