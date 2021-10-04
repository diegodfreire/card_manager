# =============================================================================
# registry - Recebe como argumento o registry (proxy) Nexus Equinix,
#            devendo utilizar o DockerHub apenas com fallback
# =============================================================================
ARG DOCKER_REGISTRY=index.docker.io
# =============================================================================
# base - Python e lista de dependências
# =============================================================================
FROM $DOCKER_REGISTRY/python:3.9 as base
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE card_manager.settings
RUN pip install --upgrade pip
RUN pip install pipenv==2020.8.13
WORKDIR /code
COPY Pipfile /code/
RUN pipenv lock


# =============================================================================
# development - Instala dependências de dev e copia o código fonte
# =============================================================================
FROM base as dev
RUN pipenv install --system --deploy --dev
COPY . /code/

# =============================================================================
# CodeFmt - verifica se o código segue o estilo black
# =============================================================================
FROM dev AS CodeFmt
RUN black --check --diff .

# =============================================================================
# DevServer - Roda o servidor da API em modo de desenvolvimento
# =============================================================================
FROM dev as DevServer
ENV DEBUG true
ENV ALLOWED_HOSTS *
ENV ELASTIC_APM_ENABLED false
CMD ["sh", "start-dev.sh"]


# =============================================================================
# production - Instala dependências de produção e copia o código fonte
# =============================================================================
FROM base as Release
RUN pipenv install --system --deploy
COPY . /code/
RUN python manage.py collectstatic --noinput

