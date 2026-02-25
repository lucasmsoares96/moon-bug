#### BASE STAGE
#### Installs moon.

FROM node:latest AS base
WORKDIR /app

# Install moon binary
RUN curl -fsSL https://moonrepo.dev/install/moon.sh | bash -s -- 2.0.1
ENV PATH="/root/.moon/bin:/root/.proto/bin:$PATH"

#### SKELETON STAGE
#### Scaffolds repository skeleton structures.

FROM base AS skeleton

# Copy entire repository and scaffold
COPY . .
RUN moon docker scaffold python_bot-backend

#### BUILD STAGE
#### Builds the project.

FROM base AS build

# Copy workspace configs
COPY --from=skeleton /app/.moon/docker/configs .

# Copy project sources
COPY --from=skeleton /app/.moon/docker/sources .

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Install dependencies
RUN moon docker setup

# Prune extraneous dependencies
RUN moon docker prune

#### START STAGE
#### Runs the project.
FROM python:3.13-slim AS start

COPY --from=build /app /app

ENV PYTHONUNBUFFERED=1
ENV PATH="/app/backend/.venv/bin/:$PATH"

WORKDIR /app/backend/apps/python_bot

# Relink .venv Python executables to use the base image's Python instead of proto's Python.
RUN rm -f /app/backend/.venv/bin/python* && \
    ln -s /usr/local/bin/python3.13 /app/backend/.venv/bin/python && \
    ln -s /usr/local/bin/python3.13 /app/backend/.venv/bin/python3 && \
    ln -s /usr/local/bin/python3.13 /app/backend/.venv/bin/python3.13

CMD ["python", "-Xfrozen_modules=off", "-m", "debugpy", "--listen", "0.0.0.0:5678", "-m", "uvicorn", "python_bot.main:app", "--host", "0.0.0.0", "--port", "2004"]
