#-*- coding: utf-8 -*-

import os
from django.core.management.base import CommandError, LabelCommand
from appllamadas.util import procesar_archivo, cdr_callback

# NOTA: Para crear un nuevo comando se hace lo siguiente:
#
# 1.- Se crea un módulo management.commands dentro de la aplicación
# 2.- Se crea un módulo por cada comando nuevo que va a existir
# 3.- Dentro del módulo del comando creamos una clase Command
# 4.- En nuestro caso heredamos de la clase LabelCommand
# 5.- Implementamos el método handle_label dentro de la clase Command
#
# El script manage.py descubre automáticamente nuevos comandos agregando
# todos los que encuentre dentro de los módulos management.commands de
# todas las aplicaciones registradas en INSTALLED_APPS.

class Command(LabelCommand):
    help = u'Importa uno o más registros CDR desde un archivo de texto'
    args = "[archivo]"
    label = u'Archivo con registros CDR'

    requires_model_validation = False
    # Can't import settings during this command, because they haven't
    # necessarily been created.
    can_import_settings = False

    def handle_label(self, archivo, **options):
        # Verificamos que el archivo existe y que es un archivo regular
        if not os.path.exists(archivo):
            mensaje = u'El archivo %s no existe.'
            raise CommandError(mensaje % archivo)
        if not os.path.isfile(archivo):
            mensaje = u'La ruta %s no corresponde a un archivo regular.'
            raise CommandError(mensaje % archivo)
        # Ahora tratemos de abrirlo para lectura
        try:
            fp = open(archivo, 'r')
        except IOError:
            mensaje = u'Error al intentar abrir el archivo %s para lectura.'
            raise CommandError(mensaje % archivo)
        print u'Procesando archivo %s... por favor, espere...' % archivo
        # Aqui procesarmos el archivo abierto, aplicando la función
        # callback a cada registro.
        contador = procesar_archivo(fp, cdr_callback)
        if contador < 1:
          print u'Ningún registro CDR fué procesado exitosamente.'
        elif contador == 1:
          print 'Se proceso 1 registro CDR exitosamente.' % contador
        elif contador > 1:
          print 'Se procesaron %d registros CDR exitosamente.' % contador
