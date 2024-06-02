from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_api.serializers import (
    BookSerializer, BookListSerializer,
    GenreSerializer, AuthorSerializer,
    CheckoutSerializer, CheckoutListSerializer,
    ReservationSerializer, ReservationListSerializer, CustomerReservationSerializer,
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


class ReserveBookView(CreateAPIView):
    serializer_class = CustomerReservationSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        book = serializer.validated_data['book']
        user = request.user

        try:
            customer = user.customer_profile
        except Customer.DoesNotExist:
            return Response({'status': 'customer_not_found'}, status=status.HTTP_400_BAD_REQUEST)

        # Checks if the customer already has an active reservation
        if Reservation.objects.filter(customer=customer).exists():
            return Response(
                data={'status': 'active_reservation_exists'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if book.stock > 0:
            reservation = Reservation.objects.create(
                book=book,
                customer=customer
            )
            book.stock -= 1
            book.save(update_fields=('stock',))

            headers = self.get_success_headers(serializer.data)
            return Response(
                data={'status': 'reserved', 'reservation_id': reservation.id},
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        else:
            return Response(
                data={'status': 'out_of_stock'},
                status=status.HTTP_400_BAD_REQUEST
            )


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
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ('book', 'customer', 'is_returned')
    ordering_fields = ('id', 'checkout_date', 'return_date', 'is_returned')


class ReservationViewSet(ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = SerializerFactory(
        default=ReservationSerializer,
        list=ReservationListSerializer
    )
    permission_classes = [IsAdminUser]
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ('book', 'customer')
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
