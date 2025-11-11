from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm


class RegisterView(CreateView):
    form_class = UserCreationForm  # Форма для регистрации, и создания пользователя в БД
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')  # перенаправление на страницу входа после успешной регистрации
