from django.db import models

class Author(models.Model):
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Genre(models.Model):
    name = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    authors = models.ManyToManyField(Author)
    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return self.title