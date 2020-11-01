FROM python:3.8-slim
RUN pip install poetry
WORKDIR /usr/src/

COPY pyproject.toml poetry.lock /usr/src/ 
RUN cd /usr/src && poetry install --no-root
COPY . /usr/src/
RUN poetry install --no-root

CMD poetry run hestia start_server -vvv
