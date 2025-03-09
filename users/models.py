from django.db import models
from django.contrib.auth.models import AbstractUser


class Subscriber(models.Model):
    email = models.EmailField(unique=True)  # Уникальное значение для email
    full_name = models.CharField(max_length=255)  # ФИО
    comment = models.TextField(blank=True, null=True)  # Комментарий

    def __str__(self):
        return self.full_name


class Message(models.Model):
    subject = models.CharField(max_length=255)  # Тема письма
    body = models.TextField()  # Тело письма

    def __str__(self):
        return self.subject


class User(models.Model):
    email = models.EmailField(unique=True)  # Уникальное значение для email
    full_name = models.CharField(max_length=255)  # ФИО
    comment = models.TextField(blank=True, null=True)  # Комментарий

    def __str__(self):
        return self.full_name


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
