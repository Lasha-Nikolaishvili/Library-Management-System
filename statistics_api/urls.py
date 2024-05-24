from django.urls import path

from statistics_api.views import (
    MostPopularBooksView, CheckoutsLastYearView, MostLateReturnsBooksView, MostLateReturnsCustomersView
)

urlpatterns = [
    path('most-popular-books/', MostPopularBooksView.as_view(), name='most-popular-books'),
    path('checkouts-last-year/', CheckoutsLastYearView.as_view(), name='checkouts-last-year'),
    path('most-late-returns-books/', MostLateReturnsBooksView.as_view(), name='most-late-returns-books'),
    path('most-late-returns-customers/', MostLateReturnsCustomersView.as_view(), name='most-late-returns-customers'),
]
