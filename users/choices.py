from django.db.models import IntegerChoices
from django.utils.translation import gettext_lazy as _


class Status(IntegerChoices):
    LIBRARIAN = 1, _("Librarian")
    CUSTOMER = 2, _("Customer")
