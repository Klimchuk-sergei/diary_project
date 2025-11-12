from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Entry

# Просмотр списка записей
class EntryListView(LoginRequiredMixin, ListView): # Просмотр только для авторизованых пользователей
    model = Entry
    context_object_name = 'entries'
    template_name = 'diary/entry_list.html'

    # Получение списка записей для текущего пользователя
    def get_queryset(self):
        return Entry.objects.filter(user=self.request.user)

# Просмотр отдельной записи
class EntryDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView): # Просмотр только для авторизованых пользователей
    model = Entry
    context_object_name = 'entry'
    template_name = 'diary/entry_detail.html'

    # Проверка, что пользователь имеет доступ к этой записи
    def test_func(self):
        entry = self.get_object()
        return entry.user == self.request.user