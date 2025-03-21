# Metal Coils Warehouse API

API для управления складом рулонов металла, разработанное с использованием FastAPI и PostgreSQL.

## Описание

Сервис предоставляет REST API для:
- Добавления новых рулонов на склад
- Удаления рулонов со склада
- Получения списка рулонов с возможностью фильтрации
- Получения статистики по рулонам за указанный период

## Установка и запуск

1. **Клонирование репозитория**

```bash
git clone https://github.com/karinaarts/metal-coils-warehouse-api.git
```

2. **Установка зависимостей с помощью Poetry**

```bash
 make install
```
или вручную:

```bash
poetry install --extras dev --extras test
```

3. **Настройка окружения**

Разверните PostgreSQL и создайте базу данных.

Создайте файл .env в корне проекта с информацией о подключении.

Например:

```bash
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=database
POSTGRES_USER=user
```

4. **Запуск сервера для разработки**

```bash
make run
```
или вручную:

```bash
poetry run uvicorn src.main:app --reload
```

### Запуск с использованием Docker

1. **Запуск с помощью Docker Compose**

```bash
make docker
```
или вручную:

```bash
docker-compose up --build
```

API будет доступно по адресу http://localhost:8000.

Документация API доступна по адресу http://localhost:8000/docs.

## Дополнительные команды

- **Запуск линтеров**

```bash
make lint
```

- **Форматирование кода**

```bash
make format
```

- **Запуск тестов**

```bash
make test
```

- **Очистка кэша**

```bash
make clean
```

