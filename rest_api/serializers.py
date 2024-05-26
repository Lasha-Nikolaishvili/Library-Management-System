from rest_framework.serializers import ModelSerializer
from library.models import Book, Genre, Author, Checkout, Reservation, Customer


class BookSerializer(ModelSerializer):

    class Meta:
        model = Book
        fields = '__all__'


class BookListSerializer(ModelSerializer):

    class Meta:
        model = Book
        fields = ('id', 'title', 'authors', 'image')


class GenreSerializer(ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'


class AuthorSerializer(ModelSerializer):

    class Meta:
        model = Author
        fields = '__all__'


class CheckoutSerializer(ModelSerializer):

    class Meta:
        model = Checkout
        fields = '__all__'


class CheckoutListSerializer(ModelSerializer):

    class Meta:
        model = Checkout
        fields = ('id', 'book', 'customer', 'is_returned')


class ReservationSerializer(ModelSerializer):

    class Meta:
        model = Reservation
        fields = '__all__'


class CustomerReservationSerializer(ModelSerializer):

    class Meta:
        model = Reservation
        fields = ('book', )


class ReservationListSerializer(ModelSerializer):

    class Meta:
        model = Reservation
        fields = ('id', 'book', 'customer')


class CustomerSerializer(ModelSerializer):

    class Meta:
        model = Customer
        fields = '__all__'


class CustomerListSerializer(ModelSerializer):

    class Meta:
        model = Customer
        fields = ('id', 'personal_number', 'email')
