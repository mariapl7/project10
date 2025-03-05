from django.core.management.base import BaseCommand
from newsletter.models import Campaign
from django.core.mail import send_mail


class Command(BaseCommand):
    help = 'Send the specified campaign'

    def add_arguments(self, parser):
        parser.add_argument('campaign_id', type=int)

    def handle(self, *args, **kwargs):
        campaign_id = kwargs['campaign_id']
        campaign = Campaign.objects.get(id=campaign_id)

        if campaign.status == 'Запущена':
            self.stdout.write('Campaign has already been sent.')
            return

        campaign.status = 'Запущена'  # Меняем статус
        campaign.save()

        recipients = campaign.recipients.all()
        subject = campaign.message.subject
        body = campaign.message.body

        for recipient in recipients:
            send_mail(
                subject,
                body,
                'from@example.com',  # Укажите свой адрес электронной почты
                [recipient.email],
                fail_silently=False,
            )

        self.stdout.write(f'Successfully sent campaign "{campaign.subject}" to {len(recipients)} recipients.')
