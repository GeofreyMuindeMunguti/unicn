FROM python:3.9

# Install poetry
RUN pip install "poetry==1.1.14" && poetry config virtualenvs.create false

RUN pip install pyopenssl

RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org pip setuptools

# Copy poetry.lock* in case it doesn't exist in the repo
COPY pyproject.toml poetry.lock* /app/

COPY .env.local /app/.env.local

WORKDIR /app/

RUN poetry install --no-root --no-dev

COPY . /app
RUN chmod +x run.sh

EXPOSE 8000

CMD ["./run.sh"]
