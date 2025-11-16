from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

# получаем встроеную модель пользователя django
User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    """форма регистрации с полем емэйл"""
    class Meta(UserCreationForm.Meta):
        model = User
        fields =UserCreationForm.Meta.fields + ('email',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError('Email обязателен')
        # Проверка уникальности email
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Такой email уже существует')
        return email