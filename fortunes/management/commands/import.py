#-*- coding: utf-8 -*-

import os
from django.core.management.base import CommandError, LabelCommand
from fortunes.util import process_file, fortune_callback
from fortunes import strings

class Command(LabelCommand):
    help = strings.IMPORT_COMMAND_HELP
    args = strings.IMPORT_COMMAND_ARGS
    label = strings.IMPORT_COMMAND_LABEL

    requires_model_validation = False
    # Can't import settings during this command, because they haven't
    # necessarily been created.
    can_import_settings = False

    def handle_label(self, archivo, **options):
        # Checking for existence
        if not os.path.exists(archivo):
            mensaje = strings.FORTUNE_FILE_DOES_NOT_EXISTENT
            raise CommandError(mensaje % archivo)
        # Checking for a regular file
        if not os.path.isfile(archivo):
            mensaje = strings.FORTUNE_FILE_NON_REGULAR
            raise CommandError(mensaje % archivo)
        # Attempting to open the file for reading
        try:
            fp = open(archivo, 'r')
        except IOError:
            mensaje = strings.FORTUNE_FILE_NON_READABLE
            raise CommandError(mensaje % archivo)
        print strings.IMPORT_COMMAND_PROCESSING % archivo
        # Process fortune file
        counter = process_file(fp, fortune_callback)
        if counter < 1:
          print strings.IMPORT_COMMAND_ZERO_PROCESSED
        elif counter == 1:
          print strings.IMPORT_COMMAND_ONE_PROCESSED
        elif counter > 1:
          print strings.IMPORT_COMMAND_MANY_PROCESSED % counter
