from django.contrib import admin
from library.models import Checkout, Reservation


class CheckoutInline(admin.TabularInline):
    model = Checkout
    fields = ('customer', 'checkout_date', 'return_date', 'expected_return_date', 'is_returned')
    readonly_fields = ('customer', 'checkout_date', 'return_date', 'expected_return_date', 'is_returned')
    extra = 0
    can_delete = False
    show_change_link = True


class ReservationInline(admin.TabularInline):
    model = Reservation
    fields = ('customer', 'reservation_date', 'expiration_date')
    readonly_fields = ('customer', 'reservation_date', 'expiration_date')
    extra = 0
    can_delete = False
    show_change_link = True
