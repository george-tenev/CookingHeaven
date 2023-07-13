FROM python:3.10.6 as base

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt
EXPOSE 5000

FROM base as test
CMD ["python", "manage.py", "test"]

FROM base as prod
ENTRYPOINT ["gunicorn","--bind", ":8000", "CookingHeaven.wsgi"]