from .models import CampaignAttempt, SentMessage


def send_campaign(campaign, user, recipient_email):
    # Создаем запись о попытке рассылки и устанавливаем успех в False
    attempt = CampaignAttempt.objects.create(campaign=campaign, user=user, success=False)

    try:
        # Если отправка успешна
        attempt.success = True  # Обновляем статус попытки на успешный
        attempt.save()  # Сохраняем изменения записи о попытке

        # Создаем запись об отправленном сообщении
        SentMessage.objects.create(campaign=campaign, recipient_email=recipient_email, success=True)

    except Exception as e:
        # Если произошла ошибка при отправке
        print(f"Ошибка при отправке сообщения: {e}")

        # Создаем запись о неуспешной попытке отправки сообщения
        SentMessage.objects.create(campaign=campaign, recipient_email=recipient_email, success=False)
