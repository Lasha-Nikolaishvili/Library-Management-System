from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
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


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminOrReadOnly]


class CheckoutViewSet(ModelViewSet):
    queryset = Checkout.objects.all()
    serializer_class = SerializerFactory(
        default=CheckoutSerializer,
        list=CheckoutListSerializer
    )
    permission_classes = [IsAdminUser]


class ReservationViewSet(ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = SerializerFactory(
        default=ReservationSerializer,
        list=ReservationListSerializer
    )
    permission_classes = [IsAdminUser]


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = SerializerFactory(
        default=CustomerSerializer,
        list=CustomerListSerializer
    )
    permission_classes = [IsAdminUser]
