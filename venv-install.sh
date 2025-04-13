#!/bin/sh

## Описание:
# Используется для локального сетапа виртуального окружения python и установки необходимых зависимостей

python3.12 -m venv .venv
. ./.venv/bin/activate
pip install poetry
poetry config virtualenvs.create false
poetry install --no-root