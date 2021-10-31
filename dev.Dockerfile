FROM python:latest

WORKDIR /projektinator

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_ENV development
ENV POETRY_HOME=/usr

# Install Poetry for managing Python packages
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python3 -
RUN poetry --version

# Change to run as non root
RUN adduser projektinator
USER projektinator

# copy install files for installing dependencies
COPY pyproject.toml poetry.lock /projektinator/

# install python dependencies
RUN poetry install --no-interaction

EXPOSE 5000

COPY . /projektinator

ENTRYPOINT [ "poetry" ]
CMD ["run","invoke","start"]