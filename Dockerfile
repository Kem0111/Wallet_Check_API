FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory in the container
WORKDIR /app

# Install dependencies
RUN python -m pip install --upgrade pip
RUN python -m pip install poetry

# Copy the current directory contents into the container at /app
COPY . .

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction

COPY docker/entrypoint.sh docker/entrypoint.sh

RUN chmod +x docker/entrypoint.sh

ENTRYPOINT ["docker/entrypoint.sh"]

CMD ["make", "start"]

# Run migrations
# RUN poetry run alembic stamp head --purge
# RUN poetry run alembic revision --autogenerate -m "Migrations"