from django.core.management.base import BaseCommand
from django.utils import timezone
from library.models import Reservation


class Command(BaseCommand):
    help = 'Cancel expired reservations'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        expired_reservations = Reservation.objects.filter(expiration_date__lt=now)

        count = expired_reservations.count()
        expired_reservations.delete()

        self.stdout.write(self.style.SUCCESS(f'Successfully canceled {count} expired reservation(s).'))
