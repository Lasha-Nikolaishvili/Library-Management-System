from django.contrib import admin
from library.admin_filters import GenreFilter, AuthorFilter, DatePublishedListFilter
from library.models import Author, Book, Genre, Customer, Checkout, Reservation
from django.utils.translation import gettext_lazy as _


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
    search_fields = ('title',)
    autocomplete_fields = ('authors', 'genres')
    list_filter = (AuthorFilter, GenreFilter, DatePublishedListFilter)
    fieldsets = (
        (None, {
            'fields': ('title', 'image')
        }),
        ('Authors and Genres', {
            'fields': ('authors', 'genres')
        }),
        ('Date and Stock', {
            'fields': ('date_published', 'stock')
        }),
    )
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


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'personal_number', 'birth_date')
    list_display_links = ('full_name',)
    search_fields = ('full_name', 'email', 'personal_number')
    list_per_page = 20
    fieldsets = (
        ('Identification', {
            'fields': ('full_name', 'personal_number', 'user')
        }),
        ('Contact Info', {
             'fields': ('email', )
        }),
        ('Other', {
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
    list_display = ('id', 'book', 'customer', 'checkout_date', 'return_date', 'is_returned')
    list_display_links = ('book', )
    list_per_page = 20
    search_fields = ('book__title', 'customer__full_name')
    list_filter = ('is_returned', )
    autocomplete_fields = ('book', 'customer')
    actions = ['mark_as_returned']

    def mark_as_returned(self, request, queryset):
        queryset.update(is_returned=True)
    mark_as_returned.short_description = _('Mark as returned')


@admin.register(Reservation)
class Reservation(admin.ModelAdmin):
    list_display = ('id', 'book', 'customer', 'reservation_date', 'expiration_date')
    list_display_links = ('book', )
    list_per_page = 20
    search_fields = ('book__title', 'customer__full_name')
    autocomplete_fields = ('book', 'customer')
    actions = ['cancel_reservation']

    def cancel_reservation(self, request, queryset):
        queryset.delete()
    cancel_reservation.short_description = _('Cancel reservation')
