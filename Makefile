RUN = poetry run
SRC_DIR = src
TEST_DIR = tests

.DEFAULT_GOAL := help

.PHONY: help install reinstall lint format test run clean

help:
	@echo "Доступные команды:"
	@echo "install - Установить зависимости"
	@echo "reinstall - Переустановить зависимости"
	@echo "lint - Проверить код"
	@echo "format - Форматировать код"
	@echo "run - Запустить сервер"
	@echo "clean - Очистить кэш"

install:
	@echo "[ \033[00;33mУстановка зависимостей \033[00m]" && poetry install --extras dev --extras test

reinstall:
	@echo "[ \033[00;33mПереустановка зависимостей \033[00m]"
	@rm -rf poetry.lock
	@poetry install --extras dev

format:
	@echo "[ \033[00;33mЗапуск ruff format \033[00m]" && $(RUN) ruff format $(SRC_DIR) $(TEST_DIR)
	@echo "[ \033[00;33mЗапуск autopep8 \033[00m]" && $(RUN) autopep8 --in-place --aggressive --recursive $(SRC_DIR) $(TEST_DIR)
	

lint:
	@echo "[ \033[00;33mЗапуск ruff check \033[00m]" && $(RUN) ruff check $(SRC_DIR) $(TEST_DIR)
	@echo "[ \033[00;33mЗапуск flake8 \033[00m]" && $(RUN) flake8 $(SRC_DIR) $(TEST_DIR)
	@echo "[ \033[00;33mЗапуск mypy \033[00m]" && $(RUN) mypy $(SRC_DIR) $(TEST_DIR)

test:
	@echo "[ \033[00;33mЗапуск тестов \033[00m]" && $(RUN) pytest

run:
	@echo "[ \033[00;33mЗапуск сервера в режиме разработки \033[00m]" && $(RUN) uvicorn $(SRC_DIR).main:app --reload

clean:
	@echo "[ \033[00;33mОчистка кэша \033[00m]"
	@rm -rf .mypy_cache .ruff_cache
	@find . -name "__pycache__" -exec rm -fr {} +

