# 🎬 YaMDb API

**YaMDb API** — backend REST API для сервиса отзывов и рейтингов произведений: фильмов, книг, музыки и другого контента.

Проект реализует полный цикл работы с контентом и пользователями: аутентификацию, управление произведениями, отзывы и оценки, комментарии, рейтинг, фильтрацию и разграничение прав доступа.

## ✨ Основные возможности

* 🔐 Регистрация и JWT-аутентификация с подтверждением email
* 👤 Ролевая модель пользователей: `user`, `moderator`, `admin`
* 🎬 CRUD для произведений, категорий и жанров
* ⭐ Отзывы с оценкой от 1 до 10 и автоматическим расчётом рейтинга
* 💬 Комментарии к отзывам
* 🔎 Фильтрация, поиск и пагинация
* 📥 Импорт данных из CSV
* 📖 Документация API через ReDoc

## 🛠 Технологии

* **Python 3.9+**
* **Django 3.2+**
* **Django REST Framework**
* **Simple JWT**
* **Django Filter**
* **SQLite / PostgreSQL**

## 🚀 Запуск проекта

### Клонирование

```bash
git clone https://github.com/oayaivaivb/api_yamdb.git
cd api_yamdb
```

### Установка зависимостей

```bash
python -m venv venv
venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

### Миграции

```bash
python manage.py migrate
```

### Запуск

```bash
python manage.py runserver
```

API будет доступно по адресу:

```text
http://127.0.0.1:8000/api/v1/
```

Документация API:

```text
http://127.0.0.1:8000/redoc/
```

## 📊 Импорт данных

Для наполнения базы используются подготовленные CSV-файлы из директории `static/data/`.

```bash
python manage.py import_csv
```

## 👥 Команда и вклад

### Александр — Team Lead / Backend Developer

**GitHub:** [oayaivaivb](https://github.com/oayaivaivb)

Отвечал за:

* архитектуру пользовательской части;
* регистрацию и JWT-аутентификацию;
* подтверждение email;
* модель пользователей и роли;
* permissions и разграничение доступа.

### Владислав — Backend Developer

**GitHub:** [gwsdfsdf](https://github.com/gwsdfsdf)

Отвечал за:

* отзывы и комментарии;
* систему оценок;
* расчёт рейтинга произведений.

### Павел — Backend Developer

**GitHub:** [Kellance](https://github.com/Kellance)

Отвечал за:

* произведения;
* категории и жанры;
* API для работы с контентом;
* импорт данных из CSV.
