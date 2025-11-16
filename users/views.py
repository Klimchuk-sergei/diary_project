from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm


class RegisterView(CreateView):
    form_class = CustomUserCreationForm  # Форма для регистрации, и создания пользователя в БД
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')  # перенаправление на страницу входа после успешной регистрации
