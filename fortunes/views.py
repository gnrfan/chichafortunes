#-*- coding: utf-8 -*-

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from django.core.urlresolvers import reverse
from django.db import connection, transaction
from django.shortcuts import get_object_or_404
from common.shortcuts import set_message
from forms import FortuneForm
from models import Fortune
import strings

# NOTA: Estas son las dos vistas que implementan las consultas
# de los dos reportes.

def index(request):
    """Main view of Chicha Fortunes app"""

    form = FortuneForm()
    fortune = None

    if request.method == 'POST':
        form = FortuneForm(data=request.POST)

        if form.is_valid():
            remote_addr = request.META.get('REMOTE_ADDR', None)
            fortune = form.save(remote_addr=remote_addr)
            set_message(strings.FORTUNE_CREATED_MSG, request)
            return HttpResponseRedirect(reverse('homepage'))

    random = Fortune.objects.random(exclude=fortune)

    return direct_to_template(
                request,
                'fortunes/index.html',
                {'form': form,
                 'random': random
                }
           )

def fortune_detail(request, fortune_id):
    """Renders fortune in detail"""
    fortune = get_object_or_404(Fortune, id=fortune_id, accepted=True, moderated=True)
    return HttpResponse(fortune.as_text(), content_type='text/plain')

def fortunes_as_text(request):
    """Renders fortunes as text file"""
    fortunes = Fortune.objects.accepted()
    return HttpResponse('\n'.join([f.as_text() for f in fortunes]), content_type='text/plain')
