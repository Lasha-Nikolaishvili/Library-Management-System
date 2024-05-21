from django.contrib import admin
from library.models import Author, Book, Genre


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('full_name',)
    search_fields = ('full_name',)
    list_per_page = 20


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('genre',)
    search_fields = ('genre',)
    list_per_page = 20


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_published', 'stock')
    list_per_page = 20
    search_fields = ('title', 'date_published', 'stock')
    list_filter = ('genres', 'authors')
    filter_horizontal = ('genres', 'authors')
    readonly_fields = ('date_published', 'stock')
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
    set_stock_to_zero.short_description = 'Set stock to zero'
