FROM python:3.9

# Install poetry
RUN pip install "poetry==1.1.13" && poetry config virtualenvs.create false

# Copy poetry.lock* in case it doesn't exist in the repo
COPY pyproject.toml poetry.lock* /app/

COPY .env.dev .env.local

WORKDIR /app/

RUN poetry install --no-root --no-dev

COPY . /app
RUN chmod +x run.sh

EXPOSE 8000

CMD ["./run.sh"]
