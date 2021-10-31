FROM python:latest

WORKDIR /projektinator

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_ENV development

# Run as non root
RUN adduser projektinator

USER projektinator

COPY pyproject.toml poetry.lock /projektinator/

# Install Poetry for managing Python packages
RUN pip3 install poetry
# install python dependencies
RUN /home/projektinator/.local/bin/poetry install --no-interaction

EXPOSE 5000

COPY . /projektinator

CMD ["/home/projektinator/.local/bin/poetry","run","invoke","start"]