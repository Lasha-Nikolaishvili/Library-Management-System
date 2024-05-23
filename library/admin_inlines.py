from django.contrib import admin
from library.models import Checkout


class CheckoutInline(admin.TabularInline):
    model = Checkout
    fields = ('customer', 'checkout_date', 'return_date', 'expected_return_date', 'is_returned')
    readonly_fields = ('customer', 'checkout_date', 'return_date', 'expected_return_date', 'is_returned')
    extra = 0
    can_delete = False
    show_change_link = True
