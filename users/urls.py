from django.urls import path
from .views import subscriber_list, subscriber_create, subscriber_update, subscriber_delete


urlpatterns = [
    path('', subscriber_list, name='subscriber_list'),
    path('add/', subscriber_create, name='subscriber_create'),
    path('edit/<int:subscriber_id>/', subscriber_update, name='subscriber_update'),
    path('delete/<int:subscriber_id>/', subscriber_delete, name='subscriber_delete'),
    path('messages/', message_list, name='message_list'),
    path('messages/add/', message_create, name='message_create'),
    path('messages/edit/<int:message_id>/', message_update, name='message_update'),
    path('messages/delete/<int:message_id>/', message_delete, name='message_delete'),
]