#-*- coding: utf-8 -*-

from django.contrib import admin

# NOTA: Necesitamos importar los modelos que queremos que se vean 
# en el admin.

from fortunes.models import Fortune

# Registra todos los modelos de las aplicaciones
admin.autodiscover()

# Registramos otros modelos que no encuentre autodiscover()
admin.site.register(Fortune)
