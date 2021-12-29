FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_ENV development
ENV POETRY_HOME=/usr

# Install Poetry for managing Python packages
RUN curl -sSL https://install.python-poetry.org | python3 -
RUN poetry --version

RUN mkdir /projektinator && chmod a+rw /projektinator 


WORKDIR /projektinator

# copy install files for installing dependencies
COPY pyproject.toml poetry.lock /projektinator/

# install python dependencies
RUN poetry install --no-interaction

EXPOSE 5000

COPY . /projektinator

ENTRYPOINT [ "poetry" ]
CMD ["run","invoke","start"]