# syntax=docker/dockerfile:1
FROM python:3.13.7-slim AS base-deps

# Default environment
ENV \
  # docker
  DOCKER_BUILDKIT=1 \
  # python:
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PYTHONDONTWRITEBYTECODE=1 \
  # pip:
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=1 \
  PIP_DEFAULT_TIMEOUT=100 \
  # poetry:
  POETRY_VERSION=2.1.4 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_IN_PROJECT=false \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_HOME="/opt/poetry" \
  PYSETUP_PATH="/opt/pysetup" \
  VENV_PATH="/opt/pysetup/.venv"

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends make libpq-dev postgresql-client

WORKDIR /home/svc/microservices

RUN groupadd -g 1000 -r svc \
    && useradd -d "/home/svc/microservices" -g svc -l -r -u 1000 svc \
    && chown svc:svc -R "/home/svc/microservices"

FROM base-deps AS builder-base

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends build-essential curl

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN --mount=type=cache,target=/root/.cache/pip \
    curl -sSL https://install.python-poetry.org | python3 -

# copy project requirement files here to ensure they will be cached.
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=cache,target=/root/.cache/pypoetry \
    poetry run pip install -U pip && poetry install --without=dev --no-interaction --no-ansi


#######################################################################
# Scratch for constant files
#######################################################################
FROM scratch AS constant-files-production

WORKDIR /home/svc/microservices

COPY ./start /home/svc/microservices
COPY ./links /home/svc/microservices/links
COPY ./apps/account /home/svc/microservices/apps/account
COPY ./apps/monxt /home/svc/microservices/apps/monxt
COPY ./apps/movie /home/svc/microservices/apps/movie
COPY ./apps/notifications /home/svc/microservices/apps/notifications
COPY ./apps/person /home/svc/microservices/apps/person
COPY ./apps/shows /home/svc/microservices/apps/shows


#######################################################################
# Scratch for constant files development
#######################################################################
FROM scratch AS constant-files-development

WORKDIR /home/svc/microservices

COPY ./start /home/svc/microservices
COPY ./links /home/svc/microservices/links
COPY ./apps/account /home/svc/microservices/apps/account
COPY ./apps/monxt /home/svc/microservices/apps/monxt
COPY ./apps/movie /home/svc/microservices/apps/movie
COPY ./apps/notifications /home/svc/microservices/apps/notifications
COPY ./apps/person /home/svc/microservices/apps/person
COPY ./apps/shows /home/svc/microservices/apps/shows


#######################################################################
# Main build for production
#######################################################################
FROM base-deps AS production
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

USER svc
WORKDIR /home/svc/microservices
COPY --from=constant-files-production --chown=svc:svc /home/svc/microservices /home/svc/microservices


#######################################################################
# Main build for development
#######################################################################
FROM base-deps AS development
WORKDIR $PYSETUP_PATH

# copy in our built poetry + venv
COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=cache,target=/root/.cache/pypoetry \
    poetry run pip install -U pip && poetry install --no-interaction --no-ansi

USER svc
WORKDIR /home/svc/microservices
COPY --from=constant-files-development --chown=svc:svc /home/svc/microservices /home/svc/microservices

#######################################################################
# apollo stage
#######################################################################
FROM node:24.7.0-slim AS apollo-production

# Default environment
ENV PATH="$PATH:/home/svc/.local/bin"
ENV NODE_ENV='production'

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && \
    apt-get install -y --no-install-recommends net-tools && \
    apt-get install -y --no-install-recommends iputils-ping && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /home/svc/apollo

COPY ./apps/apollo/package.json ./yarn.lock /home/svc/apollo/
RUN --mount=type=cache,target=/usr/local/share/.cache/yarn \
    yarn install --frozen-lockfile --production

ARG CACHEBUST=1
COPY ./apps/apollo /home/svc/apollo


#######################################################################
# nginx stage
#######################################################################
FROM nginx:1.29.3-alpine3.22-slim AS nginx-production

COPY apps/nginx/conf/nginx.conf /etc/nginx/nginx.conf
COPY apps/nginx/conf /etc/nginx
COPY apps/nginx/conf/default.conf /etc/nginx/conf.d/

ENTRYPOINT ["nginx", "-g", "daemon off;"]

#######################################################################
# Node base stage for theater builds
#######################################################################
FROM node:24.7.0-slim AS node-base

# #######################################################################
# # Main build for theater-production
# #######################################################################
FROM node-base AS theater-base
RUN --mount=type=cache,target=/var/cache/apk,sharing=locked \
    apk update \
  && apk add --no-cache libc6-compat=1.2.5-r0 \
  && rm -rf /etc/apk/cache/*
WORKDIR /app
RUN --mount=type=cache,target=/usr/local/share/.cache/yarn \
    yarn global add turbo
COPY . .
RUN turbo prune theater --docker

FROM node-base AS theater-installer
RUN --mount=type=cache,target=/var/cache/apk,sharing=locked \
    apk update \
  && apk add --no-cache libc6-compat=1.2.5-r0 \
  && rm -rf /etc/apk/cache/*
WORKDIR /app
COPY --from=theater-base /app/out/json/ .
COPY --from=theater-base /app/out/yarn.lock ./yarn.lock
RUN --mount=type=cache,target=/usr/local/share/.cache/yarn \
    yarn install --ignore-scripts

# Build the project
COPY --from=theater-base /app/out/full/ .
COPY turbo.json /app/turbo.json
RUN --mount=type=cache,target=/usr/local/share/.cache/yarn \
    yarn turbo run build --filter=theater...

FROM node-base AS theater-production
WORKDIR /app
RUN addgroup --system --gid 1001 nodejs \
    && adduser --system --uid 1001 nextjs
USER nextjs

COPY --from=theater-installer --chown=nextjs:nodejs /app/apps/theater/next.config.mjs .
COPY --from=theater-installer --chown=nextjs:nodejs /app/apps/theater/package.json .
COPY --from=theater-installer --chown=nextjs:nodejs /app/apps/theater/.next/standalone ./
COPY --from=theater-installer --chown=nextjs:nodejs /app/apps/theater/.next/static ./apps/theater/.next/static
COPY --from=theater-installer --chown=nextjs:nodejs /app/apps/theater/public ./apps/theater/public

CMD ["node", "apps/theater/server.js"]
