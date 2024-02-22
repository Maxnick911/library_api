from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from user.api.views import registration_view, logout_view, favorite_booklist, favorite_book_details

urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('register/', registration_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('favorite/list/', favorite_booklist, name='favorite-list'),
    path('favorite/book/<int:pk>', favorite_book_details, name='favorite-book-details')
]
