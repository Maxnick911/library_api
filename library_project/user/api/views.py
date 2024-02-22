from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated 
from library.api.serializers import BookSerializer
from user.api.serializers import RegistrationSerializer
from library.api.views import IsAdminOrReadOnly
from library.models import Book

@api_view(['POST',])
def logout_view(request):
    
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

@api_view(['POST',])
def registration_view(request):
    
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        
        data = {}
        
        if serializer.is_valid():
            account = serializer.save()
            
            data['response'] = 'Registration Successful'
            data['username'] = account.username
            data['email'] = account.email
            
            token = Token.objects.get(user=account).key
            data['token'] = token
        
        else:
            data = serializer.errors                
    
        return Response(data)
    
@api_view(['GET', 'POST'])
@permission_classes([IsAdminOrReadOnly, IsAuthenticated])
def favorite_booklist(request):
    if request.method == 'GET':
        user = request.user
        favorite_books = user.favorite_books.all()
        serializer = BookSerializer(favorite_books, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        try:
            book_id = request.data['book_id']
            book = Book.objects.get(pk=book_id)
            request.user.favorite_books.add(book)
            return Response({"message": "Book added to favorites."}, status=status.HTTP_201_CREATED)
        except KeyError:
            return Response({"error": "book_id field is required."}, status=status.HTTP_400_BAD_REQUEST)
        except Book.DoesNotExist:
            return Response({"error": "Book does not exist."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def favorite_book_details(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response({"error": "Book does not exist."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        is_favorite = request.user.favorite_books.filter(pk=pk).exists()
        serializer = BookSerializer(book)
        return Response({"is_favorite": is_favorite, "book": serializer.data})

    elif request.method == 'PUT':
        request.user.favorite_books.add(book)
        return Response({"message": "Book added to favorites."}, status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE':
        request.user.favorite_books.remove(book)
        return Response({"message": "Book removed from favorites."}, status=status.HTTP_204_NO_CONTENT)