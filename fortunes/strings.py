#-*- coding: utf-8 -*-

from django.utils.translation import ugettext as _

FORTUNE_DELIMITER = _(u'%')
FORTUNE_DELIMITER_BY = _(u'%% by %s')
FORTUNE_COMMENT_TEMPLATE = _(u'- %s')
FORTUNE_PERMALINK_TEMPLATE = _(u'+ Permalink: %s')

# Constants

ORIGIN_IMPORTED_STR = _(u'Importado')
ORIGIN_SUBMITTED_STR = _(u'Enviado')

# Models

FORTUNE_MODEL = _(u'Chicha fortune')
FORTUNE_MODEL_PLURAL = _(u'Chicha fortunes')

# Forms

BODY_FORM_FIELD = _(u'Texto chicha')
SUBMITTER_FORM_FIELD = _(u'Chichero')
COMMENT_FORM_FIELD = _(u'Comentario')

# Flash messages

FORTUNE_CREATED_MSG = _(u'k se añadió el chicha entry, kthx.')

# Errors

FORTUNE_DUPLICATED_ERROR = _(u'Xuxa! Hay una fortune igualita en nuestra poderosísima '
                             u'base de datos :/')

# Exceptions

FORTUNE_FILE_NON_EXISTENT = _(u'El archivo %s no existe.')
FORTUNE_FILE_NON_REGULAR = _(u'La ruta %s no corresponde con un archivo regular.')
FORTUNE_FILE_NON_READABLE= _(u'Error al intentar abrir el archivo %s para lectura.')

# Commands

IMPORT_COMMAND_HELP = _(u'Importa un archivo de fortunes')
IMPORT_COMMAND_ARGS = _(u'[file]')
IMPORT_COMMAND_LABEL = _(u'Archivo de fortunes')
IMPORT_COMMAND_PROCESSING = _(u'Procesando archivo %s... por favor, espere...')
IMPORT_COMMAND_ZERO_PROCESSED = _(u'Ningún fortune se logró procesar exitosamente :(')
IMPORT_COMMAND_ONE_PROCESSED = _(u'Se procesó 1 fortune exitosamente.')
IMPORT_COMMAND_MANY_PROCESSED = _(u'Se procesaron %d fortunes exitosamente.')
