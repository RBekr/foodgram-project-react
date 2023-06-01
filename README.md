# Проект FOOTGRAM

![FOOTGRAM workflow](https://github.com/RBekr/foodgram-project-react/actions/workflows/main.yml/badge.svg)

адрес сервера - http://foodgram-gram.ddns.net/

admin email - admin@admin.ru

admin пароль - admin


«Продуктовый помощник»: сайт, на котором пользователи будут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволит пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд. 

_Реализованные возможности при помощи API запросов:_

+ Регистрация нового юзера
+ Авторизация при помощи  токенов
+ Создавать свои рецепты из представленных ингредиентов и тегов
+ Редактировать свои рецепты
+ Просматриваривать все рецепты на сайте
+ Подписываться на других авторов
+ Добавлять рецепты в избранное и в список покупок
+ Выгружать ингредиенты в формате .pdf для рецептов из списка покупок

_Для пользователя со статусом admin реализованы следующие возможности_:
+ Добавлять, удалять и изменять данные о пользователях 
+ Добавлять, удалять и изменять все рецепты
+ Добавлять, удалять и изменять тэги и ингредиенты

_Используемые инструменты_
1. Python ^3.7
2. Docker
3. nginx
4. Django 3.2.3
5. PostgreSQL
6. React

_Шаблон наполнения .env файла_
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY = secret_key
ALLOWED_HOSTS = localhost 127.0.0.1 [::1] testserver
```

## Setup
```
$ git clone https://github.com/RBekr/foodgram-project-react.git
$ cd foodgram-project-react/infra
$ docker-compose up --build -d
$ docker-compose exec web python manage.py makemigrations
$ docker-compose exec web python manage.py migrate
$ docker-compose exec web python manage.py createsuperuser
$ docker-compose exec web python manage.py collectstatic --no-input
$ docker-compose run web python manage.py import_ingredients "data/ingredients.json"
```
## Examples

__ДОКУМЕНТАЦИЯ__
`http://localhost/api/docs/redoc.html`

Регистрация: 
`POST http://localhost/signup`

Войти на сайт: 
`POST http://localhost/signin`

`GET http://localhost/recipes`

`GET http://localhost/recipes/{title_id}/`

`POST http://localhost/recipes`

__Авторы__: [__Руслан__](https://github.com/RBekr) 
