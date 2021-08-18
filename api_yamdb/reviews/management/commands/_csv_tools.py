import csv
# import os

from django.conf import settings

import reviews.models as rev_mdl
from reviews.models import User

BASE_DIR = settings.BASE_DIR
# CUR_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# BASE_DIR = ''.join((CUR_DIR, '\\..\\..\\'))

PATH_CSV = '/static/data/'
MODELS_FILES = {
    'User': 'users',
    'Category': 'category',
    'Genre': 'genre',
    'Title': 'titles',
    'Review': 'review',
    'Comment': 'comments',
    'GenreTitle': 'genre_title',
}
CSV_EXT = '.csv'


def import_from_csv(path_csv=None, models_files=None):
    """Импорт в БД данных из файлов .csv.

    Принимает путь до файлов и словарь с соответствием файла модели.
    Если чего-то из них нет, берёт из констант.
    Импорт в порядке перечисления в словаре.
    Неуниверсальна, все данные(модели, поля ) прописаны жёстко.
    """
    if path_csv is None:
        path_csv = PATH_CSV
    if models_files is None:
        models_files = MODELS_FILES

    # model User
    # поля в csv id,username,email,role,bio,first_name,last_name
    model = User
    file_name = ''.join((BASE_DIR, path_csv, models_files['User'], CSV_EXT))
    print('\n\nВзят в работу файл: ', file_name)

    with open(file_name, encoding='utf-8') as r_file:
        file_reader = csv.reader(r_file, delimiter=",")
        count = 0
        obj_count = 0

        for row in file_reader:
            if count == 0:
                print(f'Файл содержит столбцы: {", ".join(row)}')
                file_fields = row
            else:
                line_fields = row
                object_fields = dict(zip(file_fields, line_fields))
                print(object_fields)
                try:
                    model.objects.create(**object_fields)
                    obj_count += 1
                except Exception as e:
                    print(f'Ошибка создания записи: {e}')
                    exit
            count += 1
        print(f'Всего в файле {count} строк.',
              f'В БД добавлено {obj_count} записей.')

    # model Category
    # поля в csv id,name,slug
    model = rev_mdl.Category
    file_name = ''.join(
        (BASE_DIR, path_csv, models_files['Category'], CSV_EXT)
    )
    print('\n\nВзят в работу файл: ', file_name)

    with open(file_name, encoding='utf-8') as r_file:
        file_reader = csv.reader(r_file, delimiter=",")
        count = 0
        obj_count = 0

        for row in file_reader:
            if count == 0:
                print(f'Файл содержит столбцы: {", ".join(row)}')
                file_fields = row
            else:
                line_fields = row
                object_fields = dict(zip(file_fields, line_fields))
                try:
                    model.objects.create(**object_fields)
                    obj_count += 1
                except Exception as e:
                    print(f'Ошибка создания записи: {e}')
                    exit
            count += 1

        print(f'Всего в файле {count} строк.',
              f'В БД добавлено {obj_count} записей.')

    # model Genre
    # поля в csv id,name,slug
    model = rev_mdl.Genre
    file_name = ''.join((BASE_DIR, path_csv, models_files['Genre'], CSV_EXT))
    print('\n\nВзят в работу файл: ', file_name)

    with open(file_name, encoding='utf-8') as r_file:
        file_reader = csv.reader(r_file, delimiter=",")
        count = 0
        obj_count = 0

        for row in file_reader:
            if count == 0:
                print(f'Файл содержит столбцы: {", ".join(row)}')
                file_fields = row
            else:
                line_fields = row
                object_fields = dict(zip(file_fields, line_fields))
                try:
                    model.objects.create(**object_fields)
                    obj_count += 1
                except Exception as e:
                    print(f'Ошибка создания записи: {e}')
                    exit
            count += 1

        print(f'Всего в файле {count} строк.',
              f'В БД добавлено {obj_count} записей.')

    # model Title
    # поля в csv id,name,year,category
    model = rev_mdl.Title
    file_name = ''.join((BASE_DIR, path_csv, models_files['Title'], CSV_EXT))
    print('\n\nВзят в работу файл: ', file_name)

    with open(file_name, encoding='utf-8') as r_file:
        file_reader = csv.reader(r_file, delimiter=",")
        count = 0
        obj_count = 0

        for row in file_reader:
            if count == 0:
                print(f'Файл содержит столбцы: {", ".join(row)}')
                file_fields = row
            else:
                line_fields = row
                object_fields = dict(zip(file_fields, line_fields))
                object_fields['category'] = rev_mdl.Category.objects.get(
                    pk=object_fields['category']
                )
                try:
                    model.objects.create(**object_fields)
                    obj_count += 1
                except Exception as e:
                    print(f'Ошибка создания записи: {e}')
                    exit
            count += 1

        print(f'Всего в файле {count} строк.',
              f'В БД добавлено {obj_count} записей.')

    # model Review
    # поля в csv id,title_id,text,author,score,pub_date
    model = rev_mdl.Review
    file_name = ''.join((BASE_DIR, path_csv, models_files['Review'], CSV_EXT))
    print('\n\nВзят в работу файл: ', file_name)

    with open(file_name, encoding='utf-8') as r_file:
        file_reader = csv.reader(r_file, delimiter=",")
        count = 0
        obj_count = 0

        for row in file_reader:
            if count == 0:
                print(f'Файл содержит столбцы: {", ".join(row)}')

                file_fields = list(
                    map(
                        lambda x: x.split('_id')[0] if '_id' in x else x, row
                    )
                )
            else:
                line_fields = row
                object_fields = dict(zip(file_fields, line_fields))
                object_fields['title'] = rev_mdl.Title.objects.get(
                    pk=object_fields['title']
                )
                object_fields['author'] = User.objects.get(
                    pk=object_fields['author']
                )
                try:
                    model.objects.create(**object_fields)
                    obj_count += 1
                except Exception as e:
                    print(f'Ошибка создания записи: {e}')
                    exit
            count += 1

        print(f'Всего в файле {count} строк.',
              f'В БД добавлено {obj_count} записей.')

    # model Comment
    # поля в csv id,review_id,text,author,pub_date
    model = rev_mdl.Comment
    file_name = ''.join((BASE_DIR, path_csv, models_files['Comment'], CSV_EXT))
    print('\n\nВзят в работу файл: ', file_name)

    with open(file_name, encoding='utf-8') as r_file:
        file_reader = csv.reader(r_file, delimiter=",")
        count = 0
        obj_count = 0

        for row in file_reader:
            if count == 0:
                print(f'Файл содержит столбцы: {", ".join(row)}')

                file_fields = list(
                    map(
                        lambda x: x.split('_id')[0] if '_id' in x else x, row
                    )
                )
            else:
                line_fields = row
                object_fields = dict(zip(file_fields, line_fields))
                object_fields['review'] = rev_mdl.Review.objects.get(
                    pk=object_fields['review']
                )
                object_fields['author'] = User.objects.get(
                    pk=object_fields['author']
                )
                try:
                    model.objects.create(**object_fields)
                    obj_count += 1
                except Exception as e:
                    print(f'Ошибка создания записи: {e}')
                    exit
            count += 1

        print(f'Всего в файле {count} строк.',
              f'В БД добавлено {obj_count} записей.')

    # model Title поле genres
    # поля в csv id,title_id,genre_id
    # model = rev_mdl.GenreTitle
    file_name = ''.join(
        (BASE_DIR, path_csv, models_files['GenreTitle'], CSV_EXT)
    )
    print('\n\nВзят в работу файл: ', file_name)

    with open(file_name, encoding='utf-8') as r_file:
        file_reader = csv.reader(r_file, delimiter=",")
        count = 0
        obj_count = 0

        for row in file_reader:
            if count == 0:
                print(f'Файл содержит столбцы: {", ".join(row)}')

                file_fields = list(
                    map(
                        lambda x: x.split('_id')[0] if '_id' in x else x, row
                    )
                )
            else:
                line_fields = row
                object_fields = dict(zip(file_fields, line_fields))
                object_title = rev_mdl.Title.objects.get(
                    pk=object_fields['title']
                )
                try:
                    object_title.genres.add(
                        rev_mdl.Genre.objects.get(
                            pk=object_fields['genre']
                        )
                    )

                    # model.objects.create(**object_fields)
                    obj_count += 1
                except Exception as e:
                    print(f'Ошибка создания записи: {e}')
                    exit
            count += 1

        print(f'Всего в файле {count} строк.',
              f'В БД добавлено {obj_count} записей.')


def export_to_csv():
    pass
