# -*- coding: utf-8 -*-
from django.contrib.sites.models import Site
from deps.session_messages import create_message

def get_fqdn(site_id=None):
    """Gets FQDN of the web server host"""
    return Site.objects.get_current().domain 

def set_message(message, request=None, user=None):
    """
    Sets a user message for one-time display
    """
    if user or request:
        if request:
            _user = request.user
        else:
            _user = user
        if _user.is_authenticated():
            _user.message_set.create(message=message)
        else:
            create_message(request, message)
