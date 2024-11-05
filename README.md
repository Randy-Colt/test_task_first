### Описание

**Accunting_system** позволяет организациям удобно взаимодействовать с инфраструктурой утилизации отходов.

### Стек техноогий

- Django 3.2
- Django Rest Framework 3.12
- Djoser 2.1.0

### Установка

Клонировать репозиторий:

```
git@github.com:Randy-Colt/test_task_first.git
```
Создать файл .env с подобным содержимым:
  DEBUG=True
  SQLITE=False
  POSTGRES_DB=accounting_system
  POSTGRES_USER=user
  POSTGRES_PASSWORD=password
  DB_HOST=db
  DB_PORT=5432

Создать образы и поднять докер контейнеры командой:

```
docker compose up
```

Выполнить миграции и заполнить базу данных тестовыми данными:

```
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py loaddata test_data.json
```

API проекта доступно по адресу: http://127.0.0.1:8000

### Примеры запросов

Получение списка всех хранилищ, отсортированного по возрастанию расстояния от организации:
*request:*
```
http://127.0.0.1:8000/api/storages/
```

*response (GET):*
```
[
    {
        "name": "МНО3",
        "waste": {
            "free_space": {
                "biowaste": 250,
                "glass": 0,
                "plastic": 10
            },
            "biowaste": 0,
            "glass": 0,
            "plastic": 0,
            "biowaste_max": 250,
            "glass_max": 0,
            "plastic_max": 10
        },
        "distance": 50
    },
    {
        "name": "МНО7",
        "waste": {
            "free_space": {
                "biowaste": 250,
                "glass": 0,
                "plastic": 100
            },
            "biowaste": 0,
            "glass": 0,
            "plastic": 0,
            "biowaste_max": 250,
            "glass_max": 0,
            "plastic_max": 100
        },
        "distance": 100
    }
]
```

Просмотр запасов отходов организации:
*request (GET):*
```
http://127.0.0.1:8000/api/stock/
```

*response*:
```
{
    "free_space": {
        "biowaste": 0,
        "glass": 0,
        "plastic": 0
    },
    "biowaste": 20,
    "glass": 50,
    "plastic": 60,
    "biowaste_max": 20,
    "glass_max": 50,
    "plastic_max": 60
}
```

Отправить отходы из запасов организации в ближайшие свободные хранилища:
*request (POST):*
```
http://127.0.0.1:8000/api/dumping/
```

*response:*
```
[
    {
        "name": "МНО3",
        "waste": {
            "free_space": {
                "biowaste": 230,
                "glass": 0,
                "plastic": 0
            },
            "biowaste": 20,
            "glass": 0,
            "plastic": 10,
            "biowaste_max": 250,
            "glass_max": 0,
            "plastic_max": 10
        },
        "distance": 50
    },
    {
        "name": "МНО7",
        "waste": {
            "free_space": {
                "biowaste": 250,
                "glass": 0,
                "plastic": 50
            },
            "biowaste": 0,
            "glass": 0,
            "plastic": 50,
            "biowaste_max": 250,
            "glass_max": 0,
            "plastic_max": 100
        },
        "distance": 100
    },
    {
        "name": "МНО1",
        "waste": {
            "free_space": {
                "biowaste": 0,
                "glass": 250,
                "plastic": 100
            },
            "biowaste": 0,
            "glass": 50,
            "plastic": 0,
            "biowaste_max": 0,
            "glass_max": 300,
            "plastic_max": 100
        },
        "distance": 750
    }
]
```

### Автор проекта:
Андрей Логвинов: https://github.com/Randy-Colt
