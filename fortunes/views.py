#-*- coding: utf-8 -*-

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from django.core.urlresolvers import reverse
from django.db import connection, transaction
from django.shortcuts import get_object_or_404
from helpers.shortcuts import set_message
from helpers.shortcuts import get_fqdn
from forms import FortuneForm
from models import Fortune
import strings

def index(request, template='fortunes/index.html'):
    """Main view of fortunes app"""

    form = FortuneForm()
    fortune = None

    if request.method == 'POST':
        form = FortuneForm(data=request.POST)

        if form.is_valid():
            remote_addr = request.META.get('REMOTE_ADDR', None)
            fortune = form.save(remote_addr=remote_addr)
            set_message(strings.FORTUNE_CREATED_MSG, request)
            return HttpResponseRedirect(reverse('homepage'))

    random_fortune = Fortune.objects.random(exclude=fortune)
    random_fortune_url =  'http://' + get_fqdn() + random_fortune.get_absolute_url()

    return direct_to_template(
                request,
                template,
                {'form': form,
                 'random_fortune': random_fortune,
                 'random_fortune_url': random_fortune_url
                }
           )

def fortune_detail(request, url_id):
    """Renders fortune in detail"""
    fortune = get_object_or_404(Fortune, url_id=url_id, accepted=True, moderated=True)
    return HttpResponse(fortune.as_text(), content_type='text/plain; charset="utf-8"')

def fortunes_as_text(request):
    """Renders fortunes as text file"""
    fortunes = Fortune.objects.accepted()
    return HttpResponse('\n'.join([f.as_text() for f in fortunes]), 
                         content_type='text/plain; charset="utf-8"')
