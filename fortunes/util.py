#-*- coding: utf-8 -*-

import sys
from models import Fortune
from forms import FortuneForm
import constants

def blank_fortune_record():
    return {
        'body': [],
        'comment': None,
        'submitter': None
    }

def process_file(fp, callback):
    """Process a fortune file"""
    count = 0
    record = blank_fortune_record()
    for line in fp:
        line = line.strip()
        # Detecting a comment
        if line.startswith('- '):
            record['comment'] = line[2:].strip()
        elif line.startswith('%'):
            # Delimiter detected
            # Looking for submitter information
            if line.startswith('% by '):
                record['submitter'] = line[5:].strip()
            # Joining lines in body
            record['body'] = '\n'.join(record['body'])
            # Processing the record with the callback
            if callback(record):
                count += 1
            # Generating a new blank record
            record = blank_fortune_record()
        else:
            # Appending the line to the body
            record['body'].append(line)
    # Returning the count of fortunes processed
    return count

def fortune_callback(record):
    """Process a fortune record"""
    form = FortuneForm(data=record)
    if form.is_valid():
        form.save(origin=constants.ORIGIN_IMPORTED)
        return True
    else:
        for field, messages in form.errors.items():
            for msg in messages:
                print >> sys.stderr, "ERROR en el campo '%s': %s" % (field, msg)
        return False
