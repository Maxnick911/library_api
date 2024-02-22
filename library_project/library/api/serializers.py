from rest_framework import serializers
from library.models import Author, Genre, Book

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['first_name', 'last_name']

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name']

class BookSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    authors = AuthorSerializer(many=True)
    genres = GenreSerializer(many=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'description', 'authors', 'genres']

    def create(self, validated_data):
        authors_data = validated_data.pop('authors')
        genres_data = validated_data.pop('genres')

        book = Book.objects.create(**validated_data)

        for author_data in authors_data:
            author, created = Author.objects.get_or_create(**author_data)
            book.authors.add(author)

        for genre_data in genres_data:
            genre, created = Genre.objects.get_or_create(**genre_data)
            book.genres.add(genre)

        return book

    def update(self, instance, validated_data):
        genres_to_remove = [genre for genre in instance.genres.all() if genre not in instance.genres.filter(name__in=[data['name'] for data in validated_data.get('genres', [])])]
        instance.genres.remove(*genres_to_remove)

        authors_data = validated_data.pop('authors', [])
        genres_data = validated_data.pop('genres', [])

        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)

        for author_data in authors_data:
            author = instance.authors.filter(first_name=author_data['first_name'], last_name=author_data['last_name']).first()
            if author:
                author_serializer = AuthorSerializer(author, data=author_data)
                author_serializer.is_valid(raise_exception=True)
                author_serializer.save()
            else:
                author, created = Author.objects.get_or_create(**author_data)
                instance.authors.add(author)

        for genre_data in genres_data:
            genre = instance.genres.filter(name=genre_data['name']).first()
            if genre:
                genre_serializer = GenreSerializer(genre, data=genre_data)
                genre_serializer.is_valid(raise_exception=True)
                genre_serializer.save()
            else:
                genre, created = Genre.objects.get_or_create(**genre_data)
                instance.genres.add(genre)

        instance.save()
        return instance

    def delete(self, instance):
        instance.authors.clear()
        instance.genres.clear()
        instance.delete()
