FROM python:3.11-alpine

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

ENV TK_POSTGRES_USER=fastapi
ENV TK_POSTGRES_DB=taskapi
ENV TK_POSTGRES_PASSWORD=fastapi_admin
ENV TK_POSTGRES_PORT=5432
ENV TK_POSTGRES_HOST=taskapi_db
ENV TK_APP_TITLE=TaskAPI_Management
ENV TK_APP_DESCRIPTION=Application_for_Task_management
ENV TK_APP_VERSION=0.0.1
ENV TK_PG_URI=postgresql+asyncpg://${BK_POSTGRES_USER}:${BK_POSTGRES_PASSWORD}@${BK_POSTGRES_HOST}:${BK_POSTGRES_PORT}/${BK_POSTGRES_DB}

COPY . .

EXPOSE 7000

