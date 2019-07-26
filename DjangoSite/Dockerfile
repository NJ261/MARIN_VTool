FROM python:3.7.3
ENV NAME devlopment
WORKDIR /usr/src/app
RUN apt-get update && apt-get install -y \
  binutils \
  gdal-bin \
  python-gdal
COPY 'requirements.txt' .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000 5432
CMD python manage.py runserver