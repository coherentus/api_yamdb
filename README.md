
Описание.  

**API_YAMDB** - учебный проект из курса **"Backend developer"** [Яндекс.Практикума](https://praktikum.yandex.ru/backend-developer/).



Это часть проекта api_yamdb, которая отвечает за API

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/andrey8606/api_yamdb
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

### Примеры запросов
### USERS



**Работа с отзывами пользователей:**

эндпойнт:

```
/api/v1/titles/{title_id}/reviews/
```

разрешённые HTTP-методы:

```
GET, POST, PATCH, DELETE, HEAD, OPTIONS
```

Возможные статусы ответов:

**200: - Удачное выполнение запроса**

**400: - Отсутствует обязательное поле или оно некорректно**

**401: - Необходим JWT-токен**

**403: - Нет прав доступа**

**404: - Произведение или отзыв не найден**




- чтение списка отзывов
GET /api/v1/titles/{title_id}/reviews/

- чтение конкретного отзыва
GET /api/v1/titles/{title_id}/reviews/{review_id}

Права доступа: **Доступно без токена**

в ответе:

```python
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "text": "string",
        "author": "string",
        "score": 1,
        "pub_date": "2019-08-24T14:15:22Z"
      }
    ]
  }
]
response status code 200
```
***

- создание отзыва
POST /api/v1/titles/{title_id}/reviews/
payload
```python
{
  "text": "string",
  "score": 1
}
```
Права доступа: **user, moderator, admin**

в ответе:

```python
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
response status code 200
```
***

- Изменение конкретного отзыва:

PATCH /api/v1/titles/{title_id}/reviews/{review_id}/

payload
```python
{
  "text": "string",
  "score": 1
}
```
Права доступа: **user(автор отзыва), moderator, admin**

в ответе:

```python
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
response status code 200
```
***

- Удаление конкретного отзыва:

DELETE /api/v1/titles/{title_id}/reviews/{review_id}/

payload
```python
не требуется
```
Права доступа: **user(автор отзыва), moderator, admin**

в ответе:

```python
response status code 204
```
***




**Работа с комментариями на отзывы:**

эндпойнт:

```
/api/v1/titles/{title_id}/reviews/{review_id}/comments/
```

разрешённые HTTP-методы:

```
GET, POST, PATCH, DELETE, HEAD, OPTIONS
```

Возможные статусы ответов:

**200: - Удачное выполнение запроса**

**400: - Отсутствует обязательное поле или оно некорректно**

**401: - Необходим JWT-токен**

**403: - Нет прав доступа**

**404: - Не найдено произведение, отзыв или комментарий**




- чтение списка комментариев
GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/

- чтение конкретного комментария
GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}

Права доступа: **Доступно без токена**

в ответе:

```python
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "text": "string",
        "author": "string",
        "pub_date": "2019-08-24T14:15:22Z"
      }
    ]
  }
]
response status code 200
```
***

- создание комментария
POST /api/v1/titles/{title_id}/reviews/comments/

payload
```python
{
  "text": "string"
}
```
Права доступа: **user, moderator, admin**

в ответе:

```python
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
response status code 200
```
***

- Изменение конкретного комментария:

PATCH /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}

payload
```python
{
  "text": "string"
}
```
Права доступа: **user(автор отзыва), moderator, admin**

в ответе:

```python
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
response status code 200
```
***

- Удаление конкретного комментария:

DELETE /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}

payload
```python
не требуется
```
Права доступа: **user(автор отзыва), moderator, admin**

в ответе:

```python
response status code 204
```
***


*Импорт csv-файлов*

```python
python manage.py import_csv
```