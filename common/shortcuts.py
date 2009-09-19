# -*- coding: utf-8 -*-
from deps.session_messages import create_message

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
