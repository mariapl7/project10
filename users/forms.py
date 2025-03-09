from django import forms
from .models import Subscriber, Message


class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email', 'full_name', 'comment']


class Message(models.Model):
    subject = models.CharField(max_length=255)  # Тема письма
    body = models.TextField()  # Тело письма

    def __str__(self):
        return self.subject


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']
