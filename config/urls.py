from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # авторизация, login, logout
    path('auth/', include('django.contrib.auth.urls')),
    # регистрация, профиль
    path('users/', include('users.urls', namespace='users')),
    # дневник, main page
    path('', include('diary.urls', namespace='diary')),
]
