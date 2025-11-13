from urllib import request

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Entry
from django.urls import reverse_lazy
from django.db.models import Q


# Просмотр списка записей
class EntryListView(LoginRequiredMixin, ListView):  # Просмотр только для авторизованых пользователей
    model = Entry
    context_object_name = 'entries'
    template_name = 'diary/entry_list.html'
    paginate_by = 10

    # Получение списка записей для текущего пользователя
    def get_queryset(self):
        queryset = Entry.objects.filter(user=self.request.user)

        # поиск по заголовку и тексту
        query = request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(author__icontains=query)).distinct()

        return queryset


# Просмотр отдельной записи
class EntryDetailView(LoginRequiredMixin, UserPassesTestMixin,
                      DetailView):  # Просмотр только для авторизованых пользователей
    model = Entry
    template_name = 'diary/entry_detail.html'

    # Проверка, что пользователь имеет доступ к этой записи
    def test_func(self):
        entry = self.get_object()
        return entry.user == self.request.user


# редактирование записи
class EntryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Entry
    fields = ['title', 'content']
    template_name = 'diary/entry_update.html'

    # Проверка на владельца записи
    def test_func(self):
        entry = self.get_object()
        return entry.user == self.request.user


# Удаление записи
class EntryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Entry
    template_name = 'diary/entry_delete.html'
    success_url = reverse_lazy('diary:entry_list')

    # Проверка на владельца записи
    def test_func(self):
        entry = self.get_object()
        return entry.user == self.request.user
