from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_api.serializers import (
    BookSerializer, BookListSerializer,
    GenreSerializer, AuthorSerializer,
    CheckoutSerializer, CheckoutListSerializer,
    ReservationSerializer, ReservationListSerializer,
    CustomerSerializer, CustomerListSerializer
)
from rest_api.permissions import IsAdminOrReadOnly
from rest_api.utils import SerializerFactory
from library.models import Book, Genre, Author, Checkout, Reservation, Customer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = SerializerFactory(
        default=BookSerializer,
        list=BookListSerializer
    )
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ('authors', 'genres')
    search_fields = ('title', 'authors__full_name')
    ordering_fields = ('id', 'title', 'date_published', 'stock')


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ('genre',)
    search_fields = ('genre',)
    ordering_fields = ('id', 'genre',)


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ('full_name',)
    search_fields = ('full_name',)
    ordering_fields = ('id', 'full_name',)


class CheckoutViewSet(ModelViewSet):
    queryset = Checkout.objects.all()
    serializer_class = SerializerFactory(
        default=CheckoutSerializer,
        list=CheckoutListSerializer
    )
    permission_classes = [IsAdminUser]
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ('is_returned', )
    search_fields = ('book__id', 'customer__id')
    ordering_fields = ('id', 'checkout_date', 'return_date', 'is_returned')


class ReservationViewSet(ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = SerializerFactory(
        default=ReservationSerializer,
        list=ReservationListSerializer
    )
    permission_classes = [IsAdminUser]
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('book__id', 'customer__id')
    ordering_fields = ('id', 'reservation_date', 'expiration_date')


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = SerializerFactory(
        default=CustomerSerializer,
        list=CustomerListSerializer
    )
    permission_classes = [IsAdminUser]
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ('personal_number', )
    search_fields = ('full_name', 'email')
    ordering_fields = ('id', 'full_name', 'email')
