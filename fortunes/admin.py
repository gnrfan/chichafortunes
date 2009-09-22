#-*- coding: utf-8 -*-

from django.contrib import admin

from models import Fortune

admin.autodiscover()

class FortuneOptions(admin.ModelAdmin):
    """Custom options for the Fortune model in the admin"""
    ordering = ('-created_at', 'moderated', )
    list_display = ('body', 'accepted', 'moderated', 'created_at', )
    list_filter = ('moderated', 'accepted', 'origin', )

admin.site.register(Fortune, FortuneOptions)


