#-*- coding: utf-8 -*-

from django.contrib import admin

from models import Fortune

admin.autodiscover()

# Registramos otros modelos que no encuentre autodiscover()
admin.site.register(Fortune)
