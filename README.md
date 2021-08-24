
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
Создать суперпользователя (для раздачи прав админам):

```
python3 manage.py createsuperuser
```

Запустить проект:

```
python3 manage.py runserver
```

### Алгоритм регистрации пользователей

1. Пользователь отправляет POST-запрос на добавление нового пользователя с параметрами `email` и `username` на эндпоинт `/api/v1/auth/signup/`.
2. YaMDB отправляет письмо с кодом подтверждения (`confirmation_code`) на адрес `email`.
3. Пользователь отправляет POST-запрос с параметрами `username` и `confirmation_code` на эндпоинт `/api/v1/auth/token/`, в ответе на запрос ему приходит `token` (JWT-токен).
4. При желании пользователь отправляет PATCH-запрос на эндпоинт `/api/v1/users/me/` и заполняет поля в своём профайле (описание полей — в документации).

### Пользовательские роли

- **Аноним** — может просматривать описания произведений, читать отзывы и комментарии.
- **Аутентифицированный пользователь** (`user`) — может, как и **Аноним**, читать всё, дополнительно он может публиковать отзывы и ставить оценку произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы; может редактировать и удалять **свои** отзывы и комментарии. Эта роль присваивается по умолчанию каждому новому пользователю.
- **Модератор** (`moderator`) — те же права, что и у **Аутентифицированного пользователя** плюс право удалять **любые** отзывы и комментарии.
- **Администратор** (`admin`) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
- **Суперюзер Django** — обладет правами администратора (`admin`)
***
### Authentication
jwt-token

Используется аутентификация с использованием JWT-токенов

Security Scheme Type: `API Key`

Header parameter name: `Bearer`
***
AUTH

Описание эндпоинтов:

- [Auth](api_yamdb/static/readme_files/README_Auth.md)
- [Categories](api_yamdb/static/readme_files/README_Categories.md)
- [Genres](api_yamdb/static/readme_files/README_Genres.md)
- [Titles](api_yamdb/static/readme_files/README_Titles.md)
- [Reviews](api_yamdb/static/readme_files/README_Reviews.md)
- [Comments](api_yamdb/static/readme_files/README_Comments.md)


*Импорт csv-файлов*

```python
python manage.py import_csv
```