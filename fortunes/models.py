#-*- coding: utf-8 -*-

import datetime
from random import randint
from django.db import models
from django.core.urlresolvers import reverse
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
        return "Fortune Nro. %d" % self.id

    def save(self, *args, **kwargs):
        """Addiional save logic for fortunes"""
        # Once the fortune gets marked as moderated its moderation 
        # timestamp gets saved.
        if self.moderated and self.moderated_at is None:
            self.moderated_at = datetime.datetime.now()
        return super(Fortune, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """ Returns the absolute URL for fortune """
        return reverse('fortune_detail', args=[self.id])

    def as_text(self):
        """Renders fortune as plain text"""
        #TODO: Use templates instead of simple string concatenation
        parts = []
        parts.append(self.body)
        if self.comment:
            parts.append(strings.FORTUNE_COMMENT_TEMPLATE % self.comment)
        #TODO: Use sites subframework instead of hardcoding a site
        url = 'http://fortunes.chicha.pe' + self.get_absolute_url()
        parts.append(strings.FORTUNE_PERMALINK_TEMPLATE % url)
        if self.submitter:
            parts.append(strings.FORTUNE_DELIMITER_BY % self.submitter)
        else:
           parts.append(strings.FORTUNE_DELIMITER)
        return '\n'.join(parts)

    def as_html(self):
        """Renders fortune as HTML"""
        # TODO: Use a regexp to turn URLs into actual links
        return self.as_text()
