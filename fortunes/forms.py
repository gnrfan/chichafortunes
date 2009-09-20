#-*- coding: utf-8 -*-

from django import forms
from models import Fortune
import constants
import strings

class FortuneForm(forms.Form):
    body = forms.CharField(label=strings.BODY_FORM_FIELD, 
                           max_length=65535,
                           widget=forms.widgets.Textarea,
                           required=True)
    submitter = forms.CharField(label=strings.SUBMITTER_FORM_FIELD, 
                                max_length=64, required=False)
    comment = forms.CharField(label=strings.COMMENT_FORM_FIELD, 
                              required=False)

    def clean_body(self):
        """Additional body sanitization"""
        body = self.cleaned_data['body']
        if body:
            body.strip()
        duplicates = Fortune.objects.filter(body__iexact=body).count()
        if duplicates > 0:
            raise forms.ValidationError(strings.FORTUNE_DUPLICATED_ERROR)
        return body

    def clean_submitter(self):
        """Additional body sanitization"""
        submitter = self.cleaned_data['submitter']
        if submitter:
            submitter.strip()
        return submitter

    def clean_comment(self):
        """Additional body sanitization"""
        comment = self.cleaned_data['comment']
        if comment:
            comment.strip()
        return comment

    def save(self, origin=constants.ORIGIN_SUBMITTED, 
             remote_addr=None, commit=True):
        """Creates or updates a new Fortune object"""
        self.instance = Fortune(
            body = self.cleaned_data['body'],
            submitter = self.cleaned_data['submitter'],
            comment = self.cleaned_data['comment'],
            origin = origin,
            remote_addr = remote_addr
        )
        if commit:
            self.instance.save()
        return self.instance
