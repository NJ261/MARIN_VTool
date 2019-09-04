### Requirements:
Docker, PostgreSQL, PostGIS

### Steps:
1. Make sure DB has right tables for: processed_nwp_data, unique_mmsi, communities
2. Configure your DB in settings.py: host, username, password, port.
3. Build your docker image: ```docker build -t imageName .``` (Here, dot ```.``` represents directory where your Dockerfile is).
4. Run your container: ```docker run -it --rm --net='host' -p 8000:8000 imageName``` (Here, ```--net='host'``` let us connect to machine's localhost from container to connect with local DB).

### For New Migrations
1. Get your running container's ID by: ```docker ps```.
2. Log in into your container with its ID: ```docker exec -t -i containerID bash```.
3. Apply migrations with: ```python manage.py makemigrations && python manage.py migrate```.

### Delete Old Migrations
1. Run: ```find . -path "*/migrations/*.py" -not -name "__init__.py" -delete```
2. Run: ```find . -path "*/migrations/*.pyc"  -delete```