from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipient, Message, Campaign, Client
from .forms import RecipientForm, MessageForm, CampaignForm
from django.core.mail import send_mail
from django.contrib import messages
from .models import Attempt
from .tasks import send_campaign
from .models import CampaignAttempt, SentMessage
from .decorators import user_owns_object, manager_access


def recipient_list(request):
    recipients = Recipient.objects.all()
    return render(request, 'recipient_list.html', {'recipients': recipients})


def add_recipient(request):
    if request.method == 'POST':
        form = RecipientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('recipient_list')
    else:
        form = RecipientForm()
    return render(request, 'add_recipient.html', {'form': form})


def edit_recipient(request, id):
    recipient = get_object_or_404(Recipient, id=id)
    if request.method == 'POST':
        form = RecipientForm(request.POST, instance=recipient)
        if form.is_valid():
            form.save()
            return redirect('recipient_list')
    else:
        form = RecipientForm(instance=recipient)
    return render(request, 'edit_recipient.html', {'form': form})


def delete_recipient(request, id):
    recipient = get_object_or_404(Recipient, id=id)
    if request.method == 'POST':
        recipient.delete()
        return redirect('recipient_list')
    return render(request, 'delete_recipient.html', {'recipient': recipient})


def message_list(request):    # Список сообщений
    messages = Message.objects.all()
    return render(request, 'message_list.html', {'messages': messages})


def add_message(request):     # Добавление сообщения
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('message_list')
    else:
        form = MessageForm()
    return render(request, 'add_message.html', {'form': form})


def edit_message(request, id):    # Редактирование сообщения
    message = get_object_or_404(Message, id=id)
    if request.method == 'POST':
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return redirect('message_list')
    else:
        form = MessageForm(instance=message)
    return render(request, 'edit_message.html', {'form': form})


def delete_message(request, id):    # Удаление сообщения
    message = get_object_or_404(Message, id=id)
    if request.method == 'POST':
        message.delete()
        return redirect('message_list')
    return render(request, 'delete_message.html', {'message': message})


def campaign_list(request):    # Список рассылок
    campaigns = Campaign.objects.all()
    return render(request, 'campaign_list.html', {'campaigns': campaigns})


def add_campaign(request):    # Добавление рассылки
    if request.method == 'POST':
        form = CampaignForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('campaign_list')
    else:
        form = CampaignForm()
    return render(request, 'add_campaign.html', {'form': form})


def edit_campaign(request, id):   # Редактирование рассылки
    campaign = get_object_or_404(Campaign, id=id)
    if request.method == 'POST':
        form = CampaignForm(request.POST, instance=campaign)
        if form.is_valid():
            form.save()
            return redirect('campaign_list')
    else:
        form = CampaignForm(instance=campaign)
    return render(request, 'edit_campaign.html', {'form': form})


def delete_campaign(request, id):   # Удаление рассылки
    campaign = get_object_or_404(Campaign, id=id)
    if request.method == 'POST':
        campaign.delete()
        return redirect('campaign_list')
    return render(request, 'delete_campaign.html', {'campaign': campaign})


def send_campaign(request, id):
    campaign = get_object_or_404(Campaign, id=id)

    # Проверяем статус и получателей
    if campaign.status == 'Запущена':
        messages.error(request, "Рассылка уже была отправлена.")
        return redirect('campaign_list')

    # Изменяем статус на 'Запущена'
    campaign.status = 'Запущена'
    campaign.save()

    recipients = campaign.recipients.all()
    subject = campaign.message.subject
    body = campaign.message.body

    for recipient in recipients:
        try:
            send_mail(
                subject,
                body,
                'from@example.com',  # Укажите свой адрес электронной почты
                [recipient.email],
                fail_silently=False,
            )
            # Создаем запись о успешной попытке
            Attempt.objects.create(status='Успешно', campaign=campaign)
        except Exception as e:
            # Создаем запись о неуспешной попытке с ошибкой
            Attempt.objects.create(status='Не успешно', response=str(e), campaign=campaign)

    messages.success(request, "Рассылка успешно отправлена!")
    return redirect('campaign_list')


def attempt_list(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    attempts = campaign.attempts.all()  # Получаем все попытки для выбранной рассылки
    return render(request, 'attempt_list.html', {'campaign': campaign, 'attempts': attempts})


def home(request):
    total_campaigns = Campaign.objects.count()  # Общее количество рассылок
    active_campaigns = Campaign.objects.filter(status='Запущена').count()  # Количество активных рассылок
    unique_recipients = Recipient.objects.values('email').distinct().count()  # Количество уникальных получателей

    context = {
        'total_campaigns': total_campaigns,
        'active_campaigns': active_campaigns,
        'unique_recipients': unique_recipients,
    }

    return render(request, 'home.html', context)  # home.html - ваш шаблон главной страницы


def statistics_view(request):
    user_campaigns = CampaignAttempt.objects.filter(user=request.user)

    successful_attempts = user_campaigns.filter(success=True).count()
    failed_attempts = user_campaigns.filter(success=False).count()

    total_messages_sent = SentMessage.objects.filter(campaign__in=user_campaigns.values('campaign')).count()
    successful_messages = SentMessage.objects.filter(campaign__in=user_campaigns.values('campaign'), success=True).count()
    failed_messages = SentMessage.objects.filter(campaign__in=user_campaigns.values('campaign'), success=False).count()

    context = {
        'successful_attempts': successful_attempts,
        'failed_attempts': failed_attempts,
        'total_messages_sent': total_messages_sent,
        'successful_messages': successful_messages,
        'failed_messages': failed_messages,
    }
    return render(request, 'statistics.html', context)


def send_newsletter_view(request, campaign_id):
    campaign = Campaign.objects.get(id=campaign_id)
    user = request.user
    recipient_email = 'recipient@example.com'  # Получите реальный адрес получателя

    send_campaign(campaign, user, recipient_email)

    return render(request, 'send_success.html')


def campaign_detail(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    return render(request, 'campaign_detail.html', {'campaign': campaign})


@user_owns_object(lambda id: get_object_or_404(Campaign, id=id))
def edit_campaign(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)


@manager_access
def all_campaigns(request):
    """ Представление для просмотра всех кампаний. """
    campaigns = Campaign.objects.all()  # Получаем все кампании
    return render(request, 'all_campaigns.html', {'campaigns': campaigns})


@manager_access
def all_clients(request):
    """ Представление для просмотра всех клиентов. """
    clients = Client.objects.all()  # Получаем всех клиентов
    return render(request, 'all_clients.html', {'clients': clients})
