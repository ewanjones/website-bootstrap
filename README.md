## Getting Started

1. Make a `server/.env` file with the following contents:

```
SECRET_KEY=somesecretkey
EMAIL_PASSWORD=somepassword
```

2. Run `docker-compose build`
3. Run `docker-compose up`
4. Navigate to `localhost`

To use the database, you need to run:

```
$ docker-compose exec server bash

$ python manage.py mirate
```


## Personalise

1. In `server/core/setting/base.py`, set the following items:
    - BUSINESS_NAME
2. In `server/interfaces/templates/base.html`, change the `title` tag.


## Deployment

Deployment is fairly simple at the moment, just checkout the latest code and run:

```
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up
```
