#Создание окружения и установка всех зависимостей
venv-install:
	sh ./venv-install.sh

#Запуск сервиса в первый раз
start-prod-build:
	docker compose --profile prod up --build

#Запуск сервиса в первый раз
start-prod:
	docker compose --profile prod up

#Для форматирования
format:
	black app
	ruff check app --fix

#Для проверки на форматирование
lint:
	ruff check app