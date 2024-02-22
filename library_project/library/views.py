# from django.shortcuts import render
# from .models import *
# from django.http import HttpResponse, JsonResponse
# import csv

# # Create your views here.

# # Get All Books
# def book_list(request):
#     books = Book.objects.all()
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="books.csv"'

#     writer = csv.writer(response)
#     writer.writerow(['Title', 'Author', 'Genre'])

#     for book in books:
#         author_names = ', '.join([author.__str__() for author in book.authors.all()])
#         writer.writerow([
#             book.title,
#             author_names,
#             ', '.join([genre.name for genre in book.genres.all()])
#         ])

#     return response

# # Get Single Book Information
# def book_detail(request, pk):
#     book = Book.objects.get(pk=pk)
#     data = {
#         'title': book.title,
#         'description': book.description,
#         'authors': ', '.join([author.__str__() for author in book.authors.all()]),
#         'genres': ', '.join([genre.name for genre in book.genres.all()]),
#         'available': book.available,
#     }
    
#     return JsonResponse(data)