from django.contrib import admin
from library.admin_filters import GenreFilter, AuthorFilter, DatePublishedListFilter
from library.admin_inlines import CheckoutInline
from library.models import Author, Book, Genre, Customer, Checkout, Reservation
from django.utils.translation import gettext_lazy as _
from django.utils.text import Truncator


admin.site.site_header = _('Library Management System')


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name',)
    list_display_links = ('full_name',)
    search_fields = ('full_name',)
    list_per_page = 20


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'genre',)
    list_display_links = ('genre',)
    search_fields = ('genre',)
    list_per_page = 20


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'date_published', 'stock', 'get_authors', 'get_genres')
    list_display_links = ('title', )
    list_per_page = 20
    search_fields = ('title', 'authors__full_name', 'genres__genre')
    autocomplete_fields = ('authors', 'genres')
    list_filter = (AuthorFilter, GenreFilter, DatePublishedListFilter)
    readonly_fields = ('total_checkouts', 'currently_checked_out', 'available_stock')
    fieldsets = (
        (None, {
            'fields': ('title', 'image')
        }),
        (_('Authors and Genres'), {
            'fields': ('authors', 'genres')
        }),
        (_('Date and Stock'), {
            'fields': ('date_published', 'stock')
        }),
        (_('Checkouts Information'), {
            'fields': ('total_checkouts', 'currently_checked_out', 'available_stock')
        })
    )
    inlines = [CheckoutInline]
    actions = ['set_stock_to_zero']

    def set_stock_to_zero(self, request, queryset):
        queryset.update(stock=0)
    set_stock_to_zero.short_description = _('Set stock to zero')

    def get_authors(self, obj):
        return ", ".join([author.full_name for author in obj.authors.all()])
    get_authors.short_description = _('Authors')

    def get_genres(self, obj):
        return ", ".join([genre.genre for genre in obj.genres.all()])
    get_genres.short_description = _('Genres')

    def get_queryset(self, request):
        queryset = super().get_queryset(request).prefetch_related('authors', 'genres')
        return queryset

    def total_checkouts(self, obj):
        return Checkout.objects.filter(book=obj).count()
    total_checkouts.short_description = _('Total Checkouts')

    def currently_checked_out(self, obj):
        return Checkout.objects.filter(book=obj, is_returned=False).count()
    currently_checked_out.short_description = _('Currently Checked Out')

    def available_stock(self, obj):
        return obj.stock - self.currently_checked_out(obj)
    available_stock.short_description = _('Available Stock')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'personal_number', 'birth_date')
    list_display_links = ('full_name',)
    search_fields = ('full_name', 'email', 'personal_number')
    list_per_page = 20
    fieldsets = (
        (_('Identification'), {
            'fields': ('full_name', 'personal_number', 'user')
        }),
        (_('Contact Info'), {
             'fields': ('email', )
        }),
        (_('Other'), {
            'fields': ('birth_date',)
        })
    )
    actions = ['send_email']

    def send_email(self, request, queryset):
        for customer in queryset:
            print(f'Email sent to {customer.email}')
    send_email.short_description = _('Send email')


@admin.register(Checkout)
class CheckoutAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'short_book_title', 'customer', 'checkout_date', 'expected_return_date', 'return_date', 'is_returned'
    )
    list_per_page = 20
    search_fields = ('book__title', 'customer__full_name')
    list_filter = ('is_returned', )
    autocomplete_fields = ('book', 'customer')
    readonly_fields = ('checkout_date', 'expected_return_date')
    fieldsets = (
        (None, {
            'fields': ('book', 'customer')
        }),
        (_('Dates'), {
            'fields': ('checkout_date', 'return_date', 'expected_return_date')
        }),
        (_('Status'), {
            'fields': ('is_returned', )
        })
    )
    actions = ['mark_as_returned']

    def short_book_title(self, obj):
        return Truncator(obj.book.title).chars(20)
    short_book_title.short_description = _('Book Title')

    def mark_as_returned(self, request, queryset):
        queryset.update(is_returned=True)
    mark_as_returned.short_description = _('Mark as returned')


@admin.register(Reservation)
class Reservation(admin.ModelAdmin):
    list_display = ('id', 'short_book_title', 'customer', 'reservation_date', 'expiration_date')
    list_per_page = 20
    search_fields = ('book__title', 'customer__full_name')
    autocomplete_fields = ('book', 'customer')
    actions = ['cancel_reservation']
    readonly_fields = ('reservation_date', 'expiration_date', )
    fieldsets = (
        (None, {
            'fields': ('book', 'customer')
        }),
        (_('Dates'), {
            'fields': ('reservation_date', 'expiration_date')
        })
    )

    def short_book_title(self, obj):
        return Truncator(obj.book.title).chars(20)
    short_book_title.short_description = _('Book Title')

    def cancel_reservation(self, request, queryset):
        queryset.delete()
    cancel_reservation.short_description = _('Cancel reservation')
