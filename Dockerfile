FROM python:3.11

COPY . .

RUN pip install -r requirements.txt

CMD cd app; python manage.py runserver