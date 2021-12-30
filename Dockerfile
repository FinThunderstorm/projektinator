FROM python:3.10 as base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_HOME=/usr

# Install Poetry for managing Python packages
RUN curl -sSL https://install.python-poetry.org | python3 -
RUN poetry --version

RUN mkdir /projektinator && chmod a+rw /projektinator 
WORKDIR /projektinator

COPY . /projektinator

ENTRYPOINT [ "poetry" ]

# PROD IMAGE
FROM base AS production

ENV FLASK_ENV production

RUN poetry install --no-dev --no-interaction

EXPOSE 8000
CMD ["run","gunicorn","app:app", "--bind","0.0.0.0:8000"]

# DEV IMAGE
FROM base AS dev

ENV FLASK_ENV development
ENV FLASK_APP src/app.py
ENV MODE dev

RUN poetry install --no-interaction

EXPOSE 5000
CMD ["run","invoke","start"]

# TEST
FROM dev AS test

ENV MODE test

CMD ["run","invoke","coverage-report"]