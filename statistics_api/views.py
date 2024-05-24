from django.db.models import Count, F
from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from datetime import timedelta
from library.models import Book, Checkout, Customer


class MostPopularBooksView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        most_popular_books = (
            Book.objects
                .annotate(checkout_count=Count('checkout'))
                .order_by('-checkout_count')[:10]
                .values('id', 'title', 'checkout_count')
        )
        return Response(most_popular_books, status=status.HTTP_200_OK)


class CheckoutsLastYearView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        one_year_ago = now() - timedelta(days=365)
        checkouts_last_year = (
            Checkout.objects.filter(checkout_date__gte=one_year_ago).count()
        )
        return Response({'checkouts_last_year': checkouts_last_year}, status=status.HTTP_200_OK)


class MostLateReturnsBooksView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        most_late_returns_books = (
            Book.objects.annotate(
                late_returns=Count(
                    expression='checkout',
                    filter=F('checkout__return_date') > F('checkout__expected_return_date')
                )
            ).order_by('-late_returns')[:100].values('id', 'title', 'late_returns')
        )
        return Response(most_late_returns_books, status=status.HTTP_200_OK)


class MostLateReturnsCustomersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        most_late_returns_customers = (
            Customer.objects.annotate(
                late_returns=Count(
                    expression='checkout',
                    filter=F('checkout__return_date') > F('checkout__expected_return_date')
                )
            ).order_by('-late_returns')[:100].values('id', 'full_name', 'late_returns'))
        return Response(most_late_returns_customers, status=status.HTTP_200_OK)
