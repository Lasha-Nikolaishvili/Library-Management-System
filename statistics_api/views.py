from django.db.models import Count, F, Case, When, IntegerField
from django.utils.timezone import now
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from datetime import timedelta
from library.models import Book, Checkout, Customer


class MostPopularBooksView(ListAPIView):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        most_popular_books = (
            Book.objects
                .annotate(checkout_count=Count('checkout'))
                .order_by('-checkout_count')[:10]
                .values('id', 'title', 'checkout_count')
        )
        return Response(most_popular_books, status=status.HTTP_200_OK)


class CheckoutsLastYearView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        one_year_ago = now() - timedelta(days=365)
        checkouts_last_year = (
            Checkout.objects.filter(checkout_date__gte=one_year_ago).count()
        )
        return Response({'checkouts_last_year': checkouts_last_year}, status=status.HTTP_200_OK)


class MostLateReturnsBooksView(ListAPIView):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        most_late_returns_books = (
            Book.objects.annotate(
                late_returns=Count(
                    Case(
                        When(
                            checkout__return_date__gt=F('checkout__expected_return_date'),
                            then=1
                        ),
                        output_field=IntegerField()
                    )
                )
            ).order_by('-late_returns')[:100].values('id', 'title', 'late_returns')
        )
        return Response(most_late_returns_books, status=status.HTTP_200_OK)


class MostLateReturnsCustomersView(ListAPIView):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        most_late_returns_customers = (
            Customer.objects.annotate(
                late_returns=Count(
                    Case(
                        When(
                            checkout__return_date__gt=F('checkout__expected_return_date'),
                            then=1
                        ),
                        output_field=IntegerField()
                    )
                )
            ).order_by('-late_returns')[:100].values('id', 'full_name', 'late_returns'))
        return Response(most_late_returns_customers, status=status.HTTP_200_OK)
