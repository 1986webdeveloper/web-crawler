## web crawler

## Features:
- scrap domain and find page speed data of every url in domain.

1. Clone this project from repository using below command.

```shell script
$ git clone https://github.com/1986webdeveloper/web-crawler.git
$ cd web-crawler
```

2. Create virtual environment to install dependencies.

```shell script
$ virtualenv venv -p python3
``` 

3. Activate virtual environment.

```shell script
$ source venv/bin/activate
```

4. Install all the dependencies using below command.

```shell script
(venv)$ pip install -r requirements.txt
```

5. Setup PostgreSQL
    - Install the postgresql database in your local computer from the official [site link](https://www.postgresql.org/download/).

6. Create a new database using the postgresql command line

```shell script
$ CREATE DATABASE scrapper
```

7. Change username and password for database in .env file according to your postgres configuration.
    - e.g  If your postgres username is 'ABC' and password is 'XYZ', then update .env file as
```
      DB_NAME=scrapper
      DB_USER=ABC
      DB_PASSWORD=XYZ
      DB_HOST=localhost
      DB_PORT=5432
```

8. Add other required setting in .env as following

```
      DEBUG=True

      SECRET_KEY='#$S$ieASF#$AVa3#AGE$%AYSDZSEYA#SECFA#SDAWEASF@ARYAE!!!AS#$ETG'

      EMAIL_USE_TLS=True
      EMAIL_HOST='smtp.gmail.com'
      EMAIL_HOST_USER='XYZ'
      EMAIL_HOST_PASSWORD='XYZ'
      EMAIL_PORT=587

      PAGESPEED_KEY='XYZXYZ'
      PAGESPEED_URLS='https://www.googleapis.com/pagespeedonline/v5/runPagespeed'
```

9. After creating database apply migrations using below command

```shell script
(venv)$ python manage.py migrate
```

9. Run project on server using below command:
```shell script
(venv)$ python manage.py runserver
```

And navigate to `http://127.0.0.1:8000/`.