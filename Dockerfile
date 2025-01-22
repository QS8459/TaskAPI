FROM python:3.11-alpine

WORKDIR /app

COPY . .
COPY hypercorn.toml /app/hypercorn.toml
RUN chmod 644 /app/hypercorn.toml

RUN pip install -r requirements.txt

# Enable systemd service
ENV TK_POSTGRES_USER=fastapi
ENV TK_POSTGRES_DB=taskapi
ENV TK_POSTGRES_PASSWORD=fastapi_admin
ENV TK_POSTGRES_PORT=5432
ENV TK_POSTGRES_HOST=taskapi_db
ENV TK_APP_TITLE=TaskAPI_Management
ENV TK_APP_DESCRIPTION=Application_for_Task_management
ENV TK_APP_VERSION=0.0.1
ENV TK_PG_URI=postgresql+asyncpg://${TK_POSTGRES_USER}:${TK_POSTGRES_PASSWORD}@${TK_POSTGRES_HOST}:${TK_POSTGRES_PORT}/${TK_POSTGRES_DB}

EXPOSE 7000

# CMD ["hypercorn", "-c", "/app/hypercorn.toml", "main:app"]

