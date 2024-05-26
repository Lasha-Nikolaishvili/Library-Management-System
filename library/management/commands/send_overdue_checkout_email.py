from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from library.models import Checkout
from django.conf import settings


class Command(BaseCommand):
    help = 'Send email notifications to users with overdue checkouts'

    def handle(self, *args, **kwargs):
        today = timezone.now()
        overdue_checkouts = Checkout.objects.filter(is_returned=False, expected_return_date__lt=today)

        for checkout in overdue_checkouts:
            user = checkout.customer.user
            send_mail(
                'Overdue Book Return Reminder',
                f'Dear {user.first_name},\n\n'
                f'Your checkout of "{checkout.book.title}" is overdue. '
                f'Please return it as soon as possible.\n\n'
                f'Thank you,\nYour Library Team',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )

        self.stdout.write(self.style.SUCCESS('Successfully sent overdue notifications'))
