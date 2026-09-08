FROM python:3.10

WORKDIR /app

RUN pip install --no-cache-dir gunicorn flask flask-cors

COPY Pipfile* /app/

RUN pip install --no-cache-dir pipenv && \
    pipenv requirements > requirements.txt && \
    pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "__init__:app"]
