from django.contrib import admin
from library.admin_filters import GenreFilter, AuthorFilter, DatePublishedListFilter
from library.models import Author, Book, Genre
from django.utils.translation import gettext_lazy as _


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name',)
    search_fields = ('full_name',)
    list_per_page = 20


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'genre',)
    search_fields = ('genre',)
    list_per_page = 20


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'date_published', 'stock', 'get_authors', 'get_genres')
    list_per_page = 20
    search_fields = ('title', 'date_published', 'stock')
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
