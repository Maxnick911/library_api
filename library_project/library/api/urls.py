from django.urls import path
from library.api.views import book_list, book_details, export_books_to_csv

urlpatterns = [
    path('booklist/', book_list, name='book-list'),
    path('booklist/csv/', export_books_to_csv, name='book-list-csv'),
    path('book/<int:pk>', book_details, name='book-detail'),

]
