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
