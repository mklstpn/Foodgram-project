from django.contrib import admin

from .models import Tag


class TagAdmin(admin.ModelAdmin):
    list = ('name', 'color', 'slug')


admin.site.register(Tag, TagAdmin)
