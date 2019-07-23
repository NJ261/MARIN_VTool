### Requirements:
Python3, PostgreSQL, PostGIS

### Steps:
1. Install requirements: ```pip install -r requirements.txt```
2. Config your DB in settings.py: host, username, password, port.
3. Apply migrations with: ```python manage.py makemigrations && python manage.py migrate```
4. Run the application: ```python manage.py runserver```