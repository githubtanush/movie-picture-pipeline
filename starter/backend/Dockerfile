FROM python:3.10-alpine

WORKDIR /

RUN adduser -u 1000 -D app

RUN apk update && \
    apk add \
    pcre \
    pcre-dev \
    build-base \
    gcc \
    linux-headers \
    openssl \
    libffi-dev

RUN mkdir -p /var/www/app && mkdir /app

COPY Pipfile* /app

RUN echo -e "Flask==2.2.2\nFlask-Cors==3.0.10\nuWSGI==2.0.21\npytest==7.1.3\nrequests==2.28.1" > /app/requirements.txt && \
    pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

CMD uwsgi --http :5000 --master --enable-threads -s /var/www/app/app.sock --manage-script-name --mount /=app:app
