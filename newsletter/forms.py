from django import forms
from .models import Recipient, Message, Campaign


class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ['email', 'full_name', 'comment']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']


class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['start_time', 'end_time', 'status', 'message', 'recipients']
