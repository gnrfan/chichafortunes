#-*- coding: utf-8 -*-

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from django.core.urlresolvers import reverse
from django.db import connection, transaction
from django.shortcuts import get_object_or_404
from helpers.shortcuts import set_message
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

    return direct_to_template(
                request,
                template,
                {'form': form,
                 'random_fortune': random_fortune
                }
           )

def fortune_detail(request, url_id, format='text', template='fortunes/fortune_detail.html'):
    """Renders fortune in detail"""
    fortune = get_object_or_404(Fortune, url_id=url_id, accepted=True, moderated=True)
    if format == 'text':
        return HttpResponse(fortune.as_text(), content_type='text/plain; charset="utf-8"')
    else:
        return direct_to_template(
                    request,
                    template,
                    {'fortune': fortune}
               )

def fortunes_as_text(request):
    """Renders fortunes as text file"""
    fortunes = Fortune.objects.accepted()
    return HttpResponse('\n'.join([f.as_text() for f in fortunes]), 
                         content_type='text/plain; charset="utf-8"')

def fortunes_as_html(request, template='fortunes/fortunes.html'):
    """Renders fortunes as HTML file"""
    fortunes = Fortune.objects.accepted()
    return direct_to_template(
                request,
                template,
                {'fortunes': fortunes}
           )
