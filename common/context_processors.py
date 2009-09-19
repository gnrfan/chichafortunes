#-*- coding: utf-8 -*-

from django.conf import settings

def paths(request):
    """
    Add useful path information.
    This should add the correct paths according to the specific application
    """
    return {
        'media_url': settings.MEDIA_URL
    }
