from django.urls import path
from .views import RegisterView

app_name = 'users'

urlpatterns = [
    # маршрут регитрации пользователя
    path('register/', RegisterView.as_view(), name='register'),
]
