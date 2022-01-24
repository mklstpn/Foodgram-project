# Дипломный проект курса - Foodgram

![foodgram_workflow](https://github.com/mklstpn/foodgram_workflow/actions/workflows/foodgram_workflow.yml/badge.svg)

## Описание приложения

#### Проект Foodgram являет собой сборник рецептов,  

#### где каждый пользователь может добавить собственный

#### или же подписаться на рецепты другого пользователя

#### Проект доступен на http://51.250.1.69

## Пример заполнения .env файла
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=<db_name>
POSTGRES_USER=<db_user>
POSTGRES_PASSWORD=<user_password>
DB_HOST=<container_name>
DB_PORT=<db_port>
SECRET_KEY=<django_secret_key>
```

## Как запустить проект
- Перейти в директорию /infra
- Выполнить ```docker-compose up```
- После успешного поднятия контейнеров последовательно выполнить:
```
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py loaddata dump.json
docker-compose exec backend python manage.py createsuperuser
docker-compose exec backend python manage.py collectstatic --no-input 
```

## Автор
#### Степанов Михаил