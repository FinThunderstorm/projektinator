FROM python:3.10 as base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_HOME=/usr

#RUN apt update && apt install python3-pkg-resources python3-setuptools
RUN python3 -m pip install --upgrade pip setuptools wheel invoke


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
ENV MODE production

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev --no-interaction -vvv
RUN poetry run pip install -U setuptools

EXPOSE 8000

# RUN useradd -u 8877 projektinator
# USER projektinator

CMD ["run","invoke","start-production"]

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