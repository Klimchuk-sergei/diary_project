# 📔 Личный Дневник (Personal Diary)
### Веб-приложение для ведения личного дневника. Пользователи могут регистрироваться, входить в систему, а также создавать, просматривать, редактировать и удалять (только свои) записи. Реализован функционал поиска по содержимому записей.
---
## 🛠️ Технологии и Требования

| Категория | Технологии | Статус |
| :--- | :--- | :--- |
| **Фреймворк** | Django | ✅ |
| **Стилизация** | Bootstrap 5 (CDN) | ✅ |
| **База данных** | PostgreSQL | ✅ |
| **ORM** | Django ORM | ✅ |
| **Контроль Доступа** | Permissions (Mixins) | ✅ |
| **Контейнеризация** | Docker, Docker Compose | ✅ |
| **Управление Кодом** | Git, PEP8 (стиль) | ✅ |
| **Шаблоны** | Django Templates, `widget_tweaks` | ✅ |

---

## 🚀 Установка и Запуск (Docker-Compose)

### 1. Предварительные требования

Для запуска проекта необходим установленный [Docker Desktop].

### 2. Клонирование и Настройка Git

```bash
# Клонирование проекта

git clone https://github.com/Klimchuk-sergei/diary_project.git diary_project
cd diary_project

# Переключение на основную ветку разработки
git checkout develop
```
### 3. Настройка Переменных Окружения (`.env`)

Создайте файл `.env` в корне проекта (`diary_project/`) со следующими переменными. **Замените значения на свои уникальные!**

```env
# Database Settings
POSTGRES_DB=diary_db
POSTGRES_USER=diary_user
POSTGRES_PASSWORD=strong_password 
POSTGRES_HOST=db 
POSTGRES_PORT=5432

# Django Settings
SECRET_KEY=ВАШ_СЕКРЕТНЫЙ_КЛЮЧ_ДЛЯ_DJANGO
DEBUG=True
```

### 4. Сборка и Запуск Контейнеров

Выполните команду для сборки образов и запуска сервисов:
```bush
docker-compose up --build -d
```
### 5. Инициализация Базы Данных (ORM)
```commandline
Войти в контейнер web
docker-compose exec web bash

Создать миграции (ORM)
python manage.py makemigrations diary

Применить миграции к PostgreSQL
python manage.py migrate

Создать суперпользователя
python manage.py createsuperuser 

Выйти из контейнера
exit  
```
### 6. Доступ к Приложению

    Главная страница (вход): http://localhost:8000/

    Административная панель: http://localhost:8000/admin/

### 📋 Архитектура и Функционал
Структура Приложений
*   **`config`:** Основной конфигурационный проект Django (`settings.py`, `urls.py`).
*   **`users`:** Отвечает за логику аутентификации (регистрация). Использует встроенную модель `User`.
*   **`diary`:** Основное приложение для ведения записей (модели, представления CRUD, шаблоны).

### Описание Функционала



| Название | Описание |
| :--- | :--- |
| **CRUD Записей** | Реализован через `CreateView`, `ListView`, `DetailView`, `UpdateView`, `DeleteView`. |
| **Контроль Доступа** | Пользователь может просматривать/редактировать/удалять только свои записи (`UserPassesTestMixin`). |
| **Аутентификация** | Вход/выход реализован через `django.contrib.auth.urls`. Регистрация через `users/RegisterView`. |
| **Поиск** | В `EntryListView` реализован поиск по полям `title` и `content` с использованием `Q` объектов Django ORM. |