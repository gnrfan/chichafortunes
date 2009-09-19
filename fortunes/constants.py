#-*- coding: utf-8 -*-

from django.utils.translation import ugettext as _
import strings

ORIGIN_IMPORTED = 1
ORIGIN_SUBMITTED = 2

ORIGIN_CHOICES = (
    (ORIGIN_IMPORTED, strings.ORIGIN_IMPORTED_STR),
    (ORIGIN_SUBMITTED, strings.ORIGIN_SUBMITTED_STR),
)
