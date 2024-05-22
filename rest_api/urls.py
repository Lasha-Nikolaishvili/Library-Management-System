from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_api.views import (
    BookViewSet, GenreViewSet, AuthorViewSet, CheckoutViewSet, ReservationViewSet, CustomerViewSet
)


router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')
router.register(r'genres', GenreViewSet, basename='genre')
router.register(r'authors', AuthorViewSet, basename='author')
router.register(r'checkouts', CheckoutViewSet, basename='checkout')
router.register(r'reservations', ReservationViewSet, basename='reservation')
router.register(r'customers', CustomerViewSet, basename='customer')

app_name = 'rest_api'
urlpatterns = [
    path('', include(router.urls))
]
