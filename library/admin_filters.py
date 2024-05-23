from admin_auto_filters.filters import AutocompleteFilter
from django.utils.translation import gettext_lazy as _
from django.contrib.admin import SimpleListFilter
from datetime import datetime, timedelta


class GenreFilter(AutocompleteFilter):
    title = _('Genres')
    field_name = 'genres'


class AuthorFilter(AutocompleteFilter):
    title = _('Authors')
    field_name = 'authors'


class DatePublishedListFilter(SimpleListFilter):
    title = _('Date Published')
    parameter_name = 'date_published'

    def lookups(self, request, model_admin):
        return (
            ('this_year', _('This Year')),
            ('last_year', _('Last Year')),
            ('in_last_five_years', _('In Last Five Years')),
            ('in_last_ten_years', _('In Last Ten Years')),
            ('in_last_fifty_years', _('In Last Fifty Years')),
            ('in_last_hundred_years', _('In Last Hundred Years'))
        )

    def queryset(self, request, queryset):
        today = datetime.today()
        current_year = today.year
        if self.value() == 'this_year':
            return queryset.filter(date_published__year=current_year)
        elif self.value() == 'last_year':
            return queryset.filter(date_published__year=current_year - 1)
        elif self.value() == 'in_last_five_years':
            return queryset.filter(date_published__gte=today - timedelta(days=5 * 365))
        elif self.value() == 'in_last_ten_years':
            return queryset.filter(date_published__gte=today - timedelta(days=10 * 365))
        elif self.value() == 'in_last_fifty_years':
            return queryset.filter(date_published__gte=today - timedelta(days=50 * 365))
        elif self.value() == 'in_last_hundred_years':
            return queryset.filter(date_published__gte=today - timedelta(days=100 * 365))
        return queryset
