FROM alpine as prep

ENV KOMPOSE_VERSION "v1.21.0"

RUN apk add curl

# Fetch kompose binary
RUN curl -L https://github.com/kubernetes/kompose/releases/download/$KOMPOSE_VERSION/kompose-linux-amd64 -o /tmp/kompose


FROM python:3.9-alpine

COPY --from=prep /tmp/kompose /usr/local/bin/kompose

RUN chmod +x /usr/local/bin/kompose

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --no-input
RUN python manage.py makemigrations
RUN python manage.py migrate

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
