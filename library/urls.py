from django.urls import path
from library.views import (
    index, register, login, logout, dashboard, books_listing, book_details, top_ten_books, reserve_book
)


app_name = 'library'
urlpatterns = [
    path('', index, name='index'),
    path('books/', books_listing, name='books_listing'),
    path('books/<int:book_id>', book_details, name='book_details'),
    path('top-ten-books/', top_ten_books, name='top_ten_books'),
    path('reserve/<int:book_id>/', reserve_book, name='reserve_book'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
]
