# README для API сервиса управления заметками

## Описание

Данный проект представляет собой RESTful API для сервиса управления заметками, реализованный с использованием Django REST Framework (DRF). API поддерживает функции регистрации и авторизации пользователей с использованием JWT аутентификации, а также предоставляет возможность создания, получения, редактирования и удаления заметок.

## Установка

### Предварительные требования

- Python 3.8 или выше
- pip
- Django 3.2 или выше
- Django REST Framework
- djangorestframework-simplejwt для работы с JWT

### Шаги по установке

1. **Клонируйте репозиторий:**
   bash
   git clone https://github.com/ваш_репозиторий.git
   cd ваш_репозиторий


2. **Создайте виртуальное окружение:**
   python -m venv venv
   source venv/bin/activate  # Для Windows используйте venv/Scripts/activate


3. **Установите зависимости из requirements.txt:**
   pip install -r requirements.txt
   

4. **Настройте базу данных:**

   В файле settings.py настройте параметры подключения к вашей базе данных (например, PostgreSQL, SQLite и т.д.).
   Так как основная конфигурация подключается из .env, пример его файла представлен в env_example.py

5. **Примените миграции:**
    python manage.py migrate
   

7. **Запустите сервер:**
    python manage.py runserver
   

## Использование API

### Регистрация пользователя

**POST /api/users/registration/**

**Тело запроса:**
{
    "user": {
        "username": "user1",
        "email": "user1@user.user",
        "password": "qweasdzxc"
    }
}

**Ответ:**
{
    {
    "user": {
        "email": "user1@user.user",
        "username": "user1",
        "token": "eyJ0eXAiOiJKV...."
        }
    }
}


### Авторизация пользователя

**POST /api/users/login/**

**Тело запроса:**
{
    "user": {
        "email": "email@email.email",
        "username": "admin",
        "password": "aasdasdasd"
    }
}

**Ответ:**
{
    "user": {
        "email": "email@email.email",
        "username": "admin",
        "token": "eyJ0eXAiOiJKV1Q...."
    }
}


### Обновление информации о пользователе

**PUT /api/user/update/**

**Заголовки:**
Authorization: Token access_token


**Тело запроса:**
{
    "user": {
        "username": "Mash",
        "email": "mash@user.user",
        "password": "asdasda12sdadasd"
    }
}


**Ответ:**
{
    "user": {
        "email": "mash@user.user",
        "username": "Mash",
        "token": "eyJ0eXAiOiJK....."
    }
}


### Создание заметки

**POST /api/notes/create/**

**Заголовки:**
Authorization: Token access_token


**Тело запроса:**

{
    "title": "Заголовок заметки",
    "content": "Содержимое заметки"
}


**Ответ:**
{
    "id": 1,
    "title": "Заголовок заметки",
    "content": "Содержимое заметки",
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z"
}


### Получение списка заметок

**GET /api/notes/**

**Заголовки:**
Authorization: Token access_token

[
    {
        "id": 1,
        "title": "Заголовок заметки",
        "content": "Содержимое заметки",
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-01-01T00:00:00Z"
    }
]


### Редактирование заметки

**PUT /api/notes/<int:pk>/**

**Заголовки:**
Authorization: Token access_token


**Тело запроса:**

{
    "title": "Обновленный заголовок",
    "content": "Обновленное содержимое"
}


**Ответ:**
{
    "id": 1,
    "title": "Обновленный заголовок",
    "content": "Обновленное содержимое",
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-02T00:00:00Z"
}


### Удаление заметки

**DELETE /api/notes/<int:pk>/delete/**

**Заголовки:**
Authorization: Token access_token

**Ответ:**


