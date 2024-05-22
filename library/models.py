from django.db import models
from django.contrib.auth.models import AbstractUser
from users.models import User
from django.utils.translation import gettext_lazy as _
from library.utils import default_return_date


class Customer(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='customer_profile',
        verbose_name=_('User')
    )
    email = models.EmailField(_('Name'), unique=True)
    full_name = models.CharField(_('Full Name'), max_length=255)
    personal_number = models.CharField(_('Personal Number'), max_length=11, unique=True)
    birth_date = models.DateField(_('Birth Date'))

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')


class Author(models.Model):
    full_name = models.CharField(_('Full Name'), max_length=255)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = _('Author')
        verbose_name_plural = _('Authors')
        ordering = ['full_name']


class Genre(models.Model):
    genre = models.CharField(_('Genre'), max_length=100)

    def __str__(self):
        return self.genre

    class Meta:
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')
        ordering = ['genre']


class Book(models.Model):
    authors = models.ManyToManyField(Author, related_name='books', verbose_name=_('Authors'))
    genres = models.ManyToManyField(Genre, related_name='books', verbose_name=_('Genres'))
    title = models.CharField(_('Title'), max_length=255)
    image = models.URLField(_('Image'), max_length=255)
    date_published = models.DateField(_('Date Published'))
    stock = models.PositiveIntegerField(_('Stock'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Book')
        verbose_name_plural = _('Books')
        ordering = ['-id']


class Checkout(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name=_('Book'))
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name=_('Customer'))
    checkout_date = models.DateTimeField(_('Checkout Date'), auto_now_add=True)
    return_date = models.DateTimeField(_('Return Date'), null=True, blank=True)
    expected_return_date = models.DateTimeField(_('Expected Return Date'), default=default_return_date)
    is_returned = models.BooleanField(_('Is Returned'), default=False)

    def __str__(self):
        return f'{self.book.title} checked out by {self.customer.full_name}'

    class Meta:
        verbose_name = _('Checkout')
        verbose_name_plural = _('Checkouts')
        ordering = ['-id']


class Reservation(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name=_('Book'))
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name=_('Customer'))
    reservation_date = models.DateTimeField(_('Reservation Date'), auto_now_add=True)
    expiration_date = models.DateTimeField(_('Expiration Date'))

    def __str__(self):
        return f'{self.book.title} reserved by {self.customer.full_name}'

    class Meta:
        verbose_name = _('Reservation')
        verbose_name_plural = _('Reservations')
        ordering = ['-id']
