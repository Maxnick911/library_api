from django.contrib import admin
from library.models import Author, Genre, Book

# Register your models here.
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Genre)