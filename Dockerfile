FROM alpine as prep

ENV KOMPOSE_VERSION "v1.34.0"

# To support multi-arch
ARG TARGETARCH

RUN apk add curl

# Fetch the correct kompose binary based on the target architecture
RUN curl -L https://github.com/kubernetes/kompose/releases/download/$KOMPOSE_VERSION/kompose-linux-$TARGETARCH -o /tmp/kompose

FROM python:3.13-alpine

COPY --from=prep /tmp/kompose /usr/local/bin/kompose

RUN chmod +x /usr/local/bin/kompose

WORKDIR /usr/src/app

COPY . .

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

RUN uv sync --frozen

ENV PATH="/usr/src/app/.venv/bin:$PATH"


RUN python manage.py collectstatic --no-input
RUN python manage.py makemigrations
RUN python manage.py migrate

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
