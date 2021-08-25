## USERS
Пользователи
***
![GET](../png/get.png)
### Получение списка всех пользователей
Получить список всех пользователей.

**Права доступа:** `admin`

#### url:
```
/api/v1/users/
```
#### структура JSON в отклике:
```JSON
[
    {
        "count": 0,
        "next": "string",
        "previous": "string",
        "results": [
            {
                "username": "string",
                "email": "user@example.com",
                "first_name": "string",
                "last_name": "string",
                "bio": "string",
                "role": "user"
            }
        ]
    }
]
```

Возможные коды ошибок:
`401 Необходим JWT-токен`

Может быть выполнен поиск пользователя по `username`
#### url:
```
/api/v1/users/?searh={username}
```
***
![POST](../png/post.png)
### Добавление пользователя
Добавить нового пользователя.

**Права доступа:** `admin`

*Примечание: поля `email` и `username` должны быть уникальными.*
#### url:
```
/api/v1/users/
```
#### структура JSON в запросе на добавление:
```JSON
{
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
    "role": "user"
}
```
*Обязательные поля: `username`, `email`.*

в ответе:

```python
{
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
    "role": "user"
}
```

Возможные коды ошибок:
`400 Отсутствует обязательное поле или оно некорректно`
`401 Необходим JWT-токен`
`403 Нет прав доступа`

***
![GET](../png/get.png)
### Получение пользователя по username
Получить пользователя по username.

**Права доступа:** `admin`
#### url:
```
/api/v1/users/{username}/
```

#### структура JSON в отклике:
```JSON
{
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
    "role": "user"
}
```
*Примечание: Обязательный PATH PARAMETER: `username`.*

Возможные коды ошибок:
`401 Необходим JWT-токен`
`403 Нет прав доступа`
`404 пользователь не найден`

***
![PATCH](../png/patch.png)
### Изменение данных пользователя по username
Изменить данные пользователя по username.

**Права доступа:** `admin`.

#### url:
```
/api/v1/users/{username}/
```
#### структура JSON в запросе на изменение:
```JSON
{
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
    "role": "user"
}
```
*Примечание: Обязательные поля `email` и `username` должны быть уникальными.*

*Примечание: Обязательный PATH PARAMETER: `username`.*

Примечание: значение поле `role` выбирается из списка: `user`, `moderator`, `admin`. По умолчанию `user`.

#### структура JSON в отклике:
```JSON
{
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
    "role": "user"
}
```

Возможные коды ошибок:
`400 Отсутствует обязательное поле или оно некорректно`
`401 Необходим JWT-токен`
`403 Нет прав доступа`
`404 Пользователь не найден`
***
![DELETE](../png/delete.png)
### Удаление пользователя по username
Удалить пользователя по username.
**Права доступа:** `admin`.
#### url:
```
/api/v1/users/{username}/
```
*Примечание: Обязательные PATH PARAMETERS: `username`.*

Возможные коды ошибок:
`401 Необходим JWT-токен`
`403 Нет прав доступа`
`404 Пользоваетель не найден`

***
![GET](../png/get.png)
### Получение данных своей учетной записи
Получить данные своей учетной записи

**Права доступа:** `Любой авторизованный пользователь`

#### url:
```
/api/v1/users/me/
```
#### структура JSON в отклике:
```JSON
{
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
    "role": "user"
}
```
***
![PATCH](../png/patch.png)
### Изменение данных своей учетной записи
Изменить данные своей учетной записи

**Права доступа:** `Любой авторизованный пользователь`.

#### url:
```
/api/v1/users/me/
```
#### структура JSON в запросе на изменение:
```JSON
{
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string"
}
```
*Примечание: Обязательные поля `email` и `username` должны быть уникальными.*

#### структура JSON в отклике:
```JSON
{
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
    "role": "user"
}
```

Возможные коды ошибок:
`400 Отсутствует обязательное поле или оно некорректно`
***
[Назад](../../../README.md)
