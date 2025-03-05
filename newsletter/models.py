from django.db import models
from django.contrib.auth.models import User


class Recipient(models.Model):
    email = models.EmailField(unique=True)  # Уникальное поле для email
    full_name = models.CharField(max_length=255)  # ФИО
    comment = models.TextField(blank=True, null=True)  # Комментарий

    def __str__(self):
        return self.full_name


class Message(models.Model):
    subject = models.CharField(max_length=255)  # Тема письма
    body = models.TextField()  # Тело письма

    def __str__(self):
        return self.subject


class Campaign(models.Model):
    STATUS_CHOICES = [
        ('Создана', 'Создана'),
        ('Запущена', 'Запущена'),
        ('Завершена', 'Завершена')
    ]

    start_time = models.DateTimeField()  # Дата и время первой отправки
    end_time = models.DateTimeField()    # Дата и время окончания отправки
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)  # Статус
    message = models.ForeignKey(Message, on_delete=models.CASCADE)  # Связь с моделью «Сообщение»
    recipients = models.ManyToManyField(Recipient)  # Связь с моделью «Получатель»

    def __str__(self):
        return f"Рассылка {self.message.subject} ({self.status})"


class Attempt(models.Model):
    STATUS_CHOICES = [
        ('Успешно', 'Успешно'),
        ('Не успешно', 'Не успешно'),
    ]

    timestamp = models.DateTimeField(auto_now_add=True)  # Дата и время попытки
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)  # Статус
    response = models.TextField(blank=True, null=True)  # Ответ почтового сервера
    campaign = models.ForeignKey(Campaign, related_name='attempts', on_delete=models.CASCADE)  # Внешний ключ на модель «Рассылка»

    def __str__(self):
        return f"{self.timestamp} - {self.status}"


class Campaign(models.Model):
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50)


class CampaignAttempt(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    success = models.BooleanField()  # Успех или неуспех
    timestamp = models.DateTimeField(auto_now_add=True)


class SentMessage(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    recipient_email = models.EmailField()
    sent_at = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField()  # Успешная отправка или нет


class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Campaign(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return self.title
    