from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, SAFE_METHODS
from library.models import *
from library.api.serializers import BookSerializer

from django.http import HttpResponse
import csv

class IsAdminOrReadOnly(IsAdminUser):
    def has_permission(self, request, view):
        is_admin = super(
            IsAdminOrReadOnly, 
            self).has_permission(request, view)
        return request.method in SAFE_METHODS or is_admin

@api_view(['GET', 'POST'])
@permission_classes((IsAdminOrReadOnly,))
def book_list(request):
    if request.method == 'GET':
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAdminOrReadOnly,))
def book_details(request, pk):        
    if request.method == 'GET':
        book = Book.objects.get(pk = pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    elif request.method == 'PUT':
        book = Book.objects.get(pk=pk)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
            
    elif request.method == 'DELETE':
        book = Book.objects.get(pk=pk)
        book.delete()
        return Response()

@api_view(['GET'])
@permission_classes([IsAdminUser])
def export_books_to_csv(request):
    books = Book.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="books.csv"'

    writer = csv.writer(response)
    writer.writerow(['title', 'authors', 'genres'])
    for book in books:
        authors_string = ', '.join([author.__str__() for author in book.authors.all()])
        genres_string = ', '.join([genre.name for genre in book.genres.all()])
        writer.writerow([book.title, authors_string, genres_string])

    return response 