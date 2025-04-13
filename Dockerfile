ARG PYTHON_IMAGE=python:3.12.3

FROM ${PYTHON_IMAGE}

WORKDIR /app

COPY ./data.json ./
COPY ./poetry.lock ./
COPY ./pyproject.toml ./
COPY ./start-prod.sh ./
COPY ./app ./app

ARG VENV_PATH_ARG="/opt/venv"
ENV VENV_PATH=$VENV_PATH_ARG

RUN python -m venv "$VENV_PATH"
ENV PATH="$VENV_PATH/bin:$PATH"

SHELL [ "/bin/bash", "-c" ]

RUN source "$VENV_PATH/bin/activate" && pip install poetry
RUN source "$VENV_PATH/bin/activate" && poetry config virtualenvs.create false
RUN source "$VENV_PATH/bin/activate" && poetry install -v --no-root

CMD ["bash", "./start-prod.sh"]