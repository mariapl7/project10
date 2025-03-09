from django.contrib import admin
from .models import User
from .models import Subscriber, Message


admin.site.register(User)


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'comment')
    search_fields = ('email', 'full_name')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject',)
    search_fields = ('subject',)
