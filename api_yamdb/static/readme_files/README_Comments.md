## COMMENTS
Комментарии к отзывам
***
![GET](../png/get.png)
### Получение списка всех комментариев к отзыву
Получить список всех комментариев к отзыву по id

**Права доступа:** Доступно без токена

#### url:

```
/api/v1/titles/{title_id}/reviews/{review_id}/comments/
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
                "id": 0,
                "text": "string",
                "author": "string",
                "pub_date": "2019-08-24T14:15:22Z"      
            }
        ]
    }
]
```

*Примечание: Обязательные PATH PARAMETERS `titles_id`, `review_id`.*

Возможные коды ошибок:
`404 Не найдено произведение или отзыв`
***
![POST](../png/post.png)
### Добавление комментария к отзыву
Добавить новый комментарий для отзыва.

**Права доступа:** `user`, `moderator`, `admin`

#### url:
```
/api/v1/titles/{title_id}/reviews/
```
#### структура JSON в запросе на добавление:
```JSON
{
    "text": "string"
}
```

*Примечание: Обязательные PATH PARAMETERS `titles_id`, `review_id`.*
*Обязательное поле: `text`.*

в ответе:

```python
{
    "id": 0,
    "text": "string",
    "author": "string",
    "pub_date": "2019-08-24T14:15:22Z"
}
```
`response status code 201`

Возможные коды ошибок:
`400 Отсутствует обязательное поле или оно некорректно`
#### структура JSON в отклике:
```JSON
{
    "field_name": [
    "string"
]
}
```
Другие возможные коды ошибок:
`401 Необходим JWT-токен`
`403 Нет прав доступа`
`404 Произведение не найдено`
***
![GET](../png/get.png)
### Получение комментария к отзыву
Получить комментарий для отзыва по id.

**Права доступа:** Доступно без токена
#### url:
```
/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```

#### структура JSON в отклике:
```JSON
{
    "id": 0,
    "text": "string",
    "author": "string",
    "pub_date": "2019-08-24T14:15:22Z"
}
```
*Примечание: Обязательные PATH PARAMETERS: `title_id`, `review_id`, `comment_id`.*

Возможные коды ошибок:
`404 Не найдено произведение, отзыв или комментарий`
***
![PATCH](../png/patch.png)
### Частичное обновление комментария к отзыву
Частично обновить комментарий к отзыву по id.
**Права доступа:** `Автор комментария`, `moderator` или `admin`.

#### url:
```
/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```
#### структура JSON в запросе на изменение:
```JSON
{
    "text": "string"
}
```
*Примечание: Обязательные PATH PARAMETERS: `title_id`, `review_id`, `comment_id`.*

*Примечание: Обязательное поле `text`.*
#### структура JSON в отклике:
```JSON
{
    "id": 0,
    "text": "string",
    "author": "string",
    "pub_date": "2019-08-24T14:15:22Z"
}
```

Возможные коды ошибок:
`400 Отсутствует обязательное поле или оно некорректно`
`401 Необходим JWT-токен`
`403 Нет прав доступа`
`404 Не найдено произведение, отзыв или комментарий`
***
![DELETE](../png/delete.png)
### Удаление комментария к отзыву
Удалить комментарий к отзыву по id.
**Права доступа:** `Автор комментария`, `moderator` или `admin`.
#### url:
```
/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```
*Примечание: Обязательные PATH PARAMETERS: `title_id`, `review_id`, `comment_id`.*

Возможные коды ошибок:
`401 Необходим JWT-токен`
`403 Нет прав доступа`
`404 Не найдено произведение, отзыв или комментарий`

[Назад](../../../README.md)