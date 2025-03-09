from django.shortcuts import render, redirect, get_object_or_404
from .models import Subscriber, Message
from .forms import SubscriberForm, MessageForm
from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer


def subscriber_list(request):
    subscribers = Subscriber.objects.all()
    return render(request, 'users/subscriber_list.html', {'subscribers': subscribers})


def subscriber_create(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subscriber_list')
    else:
        form = SubscriberForm()
    return render(request, 'users/subscriber_form.html', {'form': form})


def subscriber_update(request, subscriber_id):
    subscriber = get_object_or_404(Subscriber, id=subscriber_id)
    if request.method == 'POST':
        form = SubscriberForm(request.POST, instance=subscriber)
        if form.is_valid():
            form.save()
            return redirect('subscriber_list')
    else:
        form = SubscriberForm(instance=subscriber)
    return render(request, 'users/subscriber_form.html', {'form': form})


def subscriber_delete(request, subscriber_id):
    subscriber = get_object_or_404(Subscriber, id=subscriber_id)
    if request.method == 'POST':
        subscriber.delete()
        return redirect('subscriber_list')
    return render(request, 'users/subscriber_confirm_delete.html', {'subscriber': subscriber})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


def message_list(request):
    messages = Message.objects.all()
    return render(request, 'users/message_list.html', {'messages': messages})


def message_create(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('message_list')
    else:
        form = MessageForm()
    return render(request, 'users/message_form.html', {'form': form})


def message_update(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if request.method == 'POST':
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return redirect('message_list')
    else:
        form = MessageForm(instance=message)
    return render(request, 'users/message_form.html', {'form': form})


def message_delete(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if request.method == 'POST':
        message.delete()
        return redirect('message_list')
    return render(request, 'users/message_confirm_delete.html', {'message': message})