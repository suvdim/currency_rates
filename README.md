# Cервис получения котировок валют

## Структура проекта

Проект состоит из двух частей:

- **backend**: django + DRF (celery, celery-beat, redis, postgresql)
- **frontend**: vue (axios, bootstrap, jspdf, xlsx)

## Описание проекта

- курсы валют берутся с [cbr-xml-daily.ru](https://www.cbr-xml-daily.ru/daily_json.js)
- для того что бы не нагружать сторонний сервис запросами, курсы валют хранятся в бд
- списком валют можно управлять через [админку](http://localhost:8000/admin/currencies/currency/)
- для тех валют которых нет в списке, курсы добавляться не будут
- при добавлении новой валюты или сохранении изменений в сущуствующей валюте, запускается обновление курсов валют
- посмотреть список полученных валют можно в [админке](http://localhost:8000/admin/currencies/currencyrate/)
- значения курсов хранятся 7 дней (возможное использование - например показ динамики изменения курса в виде графика). При этом во фронте, пользователь видит только последние курсы валют
- новые курсы берутся раз в 5 минут (но сторониий сервис обновляет данные раз в сутки). Интервал обновления можно менять в settings.py
- для получения курсов валют и удаления устаревших используется celery
- экспорт в csv, excel и pdf реализован на фронте (возможное изменение - генерация файлов на backend для более гибкой работы с отображением содержимого файлов)

## Фронт

На [фронте](http://localhost:8080/) выводится список доступных валют.
По нажатию на кнопку “Получить котировку” формируется таблица с котировками.
Сформированную таблицу можно скачать в формате CSV, XLSX или PDF.

## Docker

Необходимо что бы были установлены [Docker](https://docs.docker.com/engine/install/) и [Docker Compose](https://docs.docker.com/compose/install/).

Создать образ и запустить контейнеры
```
COMPOSE_HTTP_TIMEOUT=200 docker-compose up -d --build
```

Добавить суперпользователя
```
docker-compose exec backend python manage.py createsuperuser
```

Добавить несколько валют (дополнительные валюты можно добавить в [админке](http://localhost:8000/admin/currencies/currency/))

```
docker-compose exec backend python manage.py loaddata currencies/fixtures/init_data.json
```

Посмотреть логи

```
docker-compose logs -f 'frontend'
```

Удалить тома вместе с контейнерами

```
docker-compose down -v
```
