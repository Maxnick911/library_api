from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('library/', include('library.api.urls')),
    path('account/', include ('user.api.urls')),
]
