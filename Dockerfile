FROM python:3.11

COPY . .

RUN pip install -r requirements.txt

CMD cd app; python manage.py runserver --noreload 0.0.0.0:8000