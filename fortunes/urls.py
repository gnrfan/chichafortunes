#-*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from admin import admin

urlpatterns = patterns('',

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    url(r'^faq$',
        direct_to_template,
        { 'template': 'fortunes/faq.html' },
        name='faq'),
)

urlpatterns += patterns('fortunes.views',
    url(r'^$',
        'index',
        name='homepage'),
    url(r'^(?P<url_id>\w+)$',
        'fortune_detail',
        name='fortune_detail'),
    url(r'^fortunes-chicha.txt$',
        'fortunes_as_text',
        name='fortunes'),
)
