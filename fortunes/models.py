#-*- coding: utf-8 -*-

import datetime
from random import randint
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.html import urlize
from helpers.shortcuts import get_fqdn
from helpers.utils import create_url_id
import exceptions
import constants
import strings

# Create your models here.

class FortuneManager(models.Manager):

    def accepted(self):
        """Retrieves only fortunes that have been approved"""
        return self.filter(moderated=True, 
                           accepted=True).order_by('id')

    def rejected(self):
        """Retrieves only fortunes pending moderation"""
        return self.filter(moderated=True, 
                           accepted=False).order_by('-moderated_at')

    def pending_moderation(self):
        """Retrieves only fortunes pending moderation"""
        return self.filter(moderated=False).order_by('-created_at')

    def random(self, exclude=None):
        """Retrieves a random Fortune"""
        result  = self.accepted()
        if exclude:
            result = result.exclude(id=exclude.id)
        num_fortunes = result.count()
        if num_fortunes > 0:
            return result[randint(0, num_fortunes-1)]
        else:
            return result
        
class Fortune(models.Model):
    # the url_id can't be a unique field because at some point will be
    # saved with a NULL value.
    url_id = models.CharField(max_length=16, blank=True, editable=False)
    body = models.TextField()
    comment = models.CharField(max_length=128, blank=True, null=True)
    submitter = models.CharField(max_length=64, blank=True, null=True)
    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    moderated = models.BooleanField(default=False)
    moderated_at = models.DateTimeField(blank=True, null=True)
    origin = models.PositiveIntegerField(choices=constants.ORIGIN_CHOICES)
    remote_addr = models.IPAddressField(blank=True, null=True)

    objects = FortuneManager()
        
    class Meta:
        verbose_name = strings.FORTUNE_MODEL
        verbose_name_plural = strings.FORTUNE_MODEL_PLURAL

    def __unicode__(self):
        stats = self.wordcount_stats()
        lines = ''
        if stats['lines'] > 1:
            lines = ' + %d lines' % stats['lines']
        return "Fortune %d (%s) - %s...%s" % (self.id, self.url_id, self.body[:48], lines)

    def save(self, *args, **kwargs):
        """Addiional save logic for fortunes"""
        # Once the fortune gets marked as moderated its moderation 
        # timestamp gets saved.
       
        # Initial save 
        if not self.id:        
            super(Fortune, self).save(*args, **kwargs)

        # Adding url_id
        if self.id and not self.url_id:
            self.url_id = create_url_id(self.id)
        
        # Here we add the moderation timestamp the first
        # time the object is saved with the 'moderated'
        # property set to True
        if self.moderated and self.moderated_at is None:
            self.moderated_at = datetime.datetime.now()

        # Returning the instance
        return super(Fortune, self).save(*args, **kwargs)

    def accept(self):
        """Moderates the fortune as accepted"""
        self.accepted = True
        self.moderated = True
        self.save()

    def reject(self):
        """Moderates the fortune as rejected"""
        self.accepted = False
        self.moderated = True
        self.save()

    def get_absolute_url(self):
        """Returns the absolute URL for fortune"""
        return reverse('fortune_detail', args=[self.url_id])

    def permalink(self):
        """Returns the full permalink to the fortune"""
        return 'http://' + get_fqdn() + self.get_absolute_url()

    def as_text(self):
        """Renders fortune as plain text"""
        #TODO: Use templates instead of simple string concatenation
        parts = []
        parts.append(self.body)
        if self.comment:
            parts.append(strings.FORTUNE_COMMENT_TEMPLATE % self.comment)
        if self.submitter:
            parts.append(strings.FORTUNE_DELIMITER_BY % self.submitter)
        else:
           parts.append(strings.FORTUNE_DELIMITER)
        return '\n'.join(parts)

    def as_html(self, autoescape=True):
        """Renders fortune as HTML"""
        value = self.as_text()
        value = urlize(value, nofollow=False, autoescape=autoescape)
        return value

    def wordcount_stats(self):
        """Returns the number of chars, words and lines in the body 
           of the fortune"""
        chars = len(self.body)
        words = len([p for p in self.body.split(' ') if len(p.strip())>0])
        lines = len(self.body.split('\n'))
        return {
            'chars': chars,
            'words': words,
            'lines': lines
        }
