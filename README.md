### api_yamdb

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
## USERS

Получение списка всех пользователей (GET):

```
http://127.0.0.1:8000/api/v1/users/
```

Добавление пользователя (POST):

```
http://127.0.0.1:8000/api/v1/users/
```

Получение пользователя по username (GET):

```
http://127.0.0.1:8000/api/v1/users/{username}/
```

Изменение данных пользователя по username (PATCH):

```
http://127.0.0.1:8000/api/v1/users/{username}/
```

даление пользователя по username (DELETE):

```
http://127.0.0.1:8000/api/v1/users/{username}/
```

Получение данных своей учетной записи (GET):

```
http://127.0.0.1:8000/api/v1/users/me/
```

Изменение данных своей учетной записи (PATCH):

```
http://127.0.0.1:8000/api/v1/users/me/
```

Регистрация нового пользователя (POST):

```
http://127.0.0.1:8000/api/v1/auth/signup/
```

Получение JWT-токена (POST):

```
http://127.0.0.1:8000/api/v1/auth/token/
```


