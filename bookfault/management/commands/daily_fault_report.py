from django.core.management.base import BaseCommand
from bookfault.send_sms import get_non_restored_faults_summary,send_whatsapp_message


class Command(BaseCommand):
    help = 'Send daily WhatsApp report of non-restored faults'

    def handle(self, *args, **kwargs):
        # Fetch non-restored faults grouped by SDCA
        summary1,summary2 = get_non_restored_faults_summary()

        # Send the message via WhatsApp
        message_sid = send_whatsapp_message(summary1)
        message_sid = send_whatsapp_message(summary2)

        self.stdout.write(self.style.SUCCESS(f'Daily fault report sent via WhatsApp. SID: {message_sid}'))
