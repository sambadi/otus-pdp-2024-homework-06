FROM python:3.12-slim

WORKDIR /app
COPY . /app

RUN pip install poetry==1.8.3 && poetry install --without dev

CMD ["poetry", "run", "python", "-m", "homework_06"]