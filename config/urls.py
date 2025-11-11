from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),  # авторизация, login, logout
    path('users/', include('users.urls', namespace='users')),  # регистрация, профиль
    path('', include('diary.urls', namespace='diary')),  # дневник, main page
]
