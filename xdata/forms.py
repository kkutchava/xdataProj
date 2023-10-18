from collections.abc import Mapping
from typing import Any
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import Clients, Notifications, Filterwords, Sites, Articles

class ClientsForm(forms.ModelForm):
    #to make integer field appear as a toggle form
    #I am not changing DB, so I am changing its appearence
    tts_enabled = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'toggle-switch'}),
        required=False
    )
    #similar idea for filterwords ID
    filterwordsid = forms.IntegerField(
        widget=forms.Select(choices=[(fw.id, fw) for fw in Filterwords.objects.all()]),
        required=False,
        label='Filter Words ID',
    )
    # for site ID
    siteid = forms.IntegerField(
        widget=forms.Select(choices=[(site.id, site) for site in Sites.objects.all()]),
        required=False,
        label='Site ID',
    )
    
    class Meta:
        model = Clients
        fields = ['username', 'siteid', 'filterwordsid', 'tts_enabled']
        labels = {
            'username': 'User Name',
            'siteid': 'Site ID',
            'filterwordsid': 'Filter Words ID',
            'tts_enabled': 'TTS Enabled',
        }
    
    # costumization to make empty fields, seen as 'select'
    def __init__(self, *args, **kwargs):
        super(ClientsForm, self).__init__(*args, **kwargs)
        # Set the initial value to None or an empty string
        self.initial['filterwordsid'] = None
        self.initial['siteid'] = None

        self.fields['filterwordsid'].empty_label = 'Choose'
        self.fields['siteid'].empty_label = 'Choose'


class NotificationsForm(forms.ModelForm):
    class Meta:
        model = Notifications
        fields = ['sms', 'telegram', 'whatsapp', 'email', 'comment']
        labels = {
            'sms': 'SMS',
            'telegram': 'Telegram',
            'whatsapp': 'WhatsApp',
            'email': 'Email',
            'comment': 'Comment'
        }

    def save(self, commit=True, client=None):
        notification = super(NotificationsForm, self).save(commit=False)
        
        # Here, you can set fields based on the associated client
        if client:
            notification.clientid = client.id
        
        if commit:
            notification.save()

        return notification
    

class FilterwordsForm(forms.ModelForm):
    class Meta:
        model = Filterwords
        fields = ['word', 'wordalias', 'subwordalias', 'stopword']
        labels = {
            'word': 'Word',
            'wordalias': 'Word Alias',
            'subwordalias': 'Sub-word Alias',
            'stopword': 'Stop-Word',
        }

    def save(self, commit=True, client=None):
        Filterword = super(FilterwordsForm, self).save(commit=False)
        
        # set fields based on the associated client
        if client:
            Filterword.clientid = client.id
        
        if commit:
            Filterword.save()

        return Filterword