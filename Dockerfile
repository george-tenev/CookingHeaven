FROM python:3.10.6 as base

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt
EXPOSE 8080

FROM base as prod
ENTRYPOINT ["gunicorn","--bind", "0.0.0.0:8080", "CookingHeaven.wsgi"]