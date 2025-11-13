from django.urls import path
from .views import (
    EntryListView, EntryDetailView, EntryCreateView,
    EntryUpdateView, EntryDeleteView
)

app_name = 'diary'

urlpatterns = [
    # Главная страница / Список записей (и поиск)
    path('', EntryListView.as_view(), name='entry_list'),

    # Создание
    path('new/', EntryCreateView.as_view(), name='entry_create'),

    # Просмотр
    path('<int:pk>/', EntryDetailView.as_view(), name='entry_detail'),

    # Редактирование
    path('<int:pk>/edit/', EntryUpdateView.as_view(), name='entry_update'),

    # Удаление
    path('<int:pk>/delete/', EntryDeleteView.as_view(), name='entry_delete'),
]
