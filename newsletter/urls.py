from django.urls import path
from .views import add_recipient, edit_recipient, delete_recipient, recipient_list
from .views import add_message, edit_message, delete_message, message_list
from .views import add_campaign, edit_campaign, delete_campaign, campaign_list, send_campaign, attempt_list, home
from .views import statistics_view
from .views import all_campaigns, all_clients


urlpatterns = [
    path('recipients/new/', add_recipient, name='add_recipient'),
    path('recipients/', recipient_list, name='recipient_list'),
    path('recipients/edit/<int:id>/', edit_recipient, name='edit_recipient'),
    path('recipients/delete/<int:id>/', delete_recipient, name='delete_recipient'),
    path('messages/', message_list, name='message_list'),
    path('messages/new/', add_message, name='add_message'),
    path('messages/edit/<int:id>/', edit_message, name='edit_message'),
    path('messages/delete/<int:id>/', delete_message, name='delete_message'),
    path('', home, name='home'),  # Главная страница
    path('campaigns/', campaign_list, name='campaign_list'),
    path('campaigns/new/', add_campaign, name='add_campaign'),
    path('campaigns/edit/<int:id>/', edit_campaign, name='edit_campaign'),
    path('campaigns/delete/<int:id>/', delete_campaign, name='delete_campaign'),
    path('campaigns/send/<int:id>/', send_campaign, name='send_campaign'),  # Новый маршрут для отправки
    path('campaigns/<int:campaign_id>/attempts/', attempt_list, name='attempt_list'),  # Новый маршрут для списка попыток
    path('statistics/', statistics_view, name='statistics'),
    path('campaigns/', all_campaigns, name='all_campaigns'),
    path('clients/', all_clients, name='all_clients'),
]