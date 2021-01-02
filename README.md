## Getting Started

1. Make a `server/.env` file (nothing in it yet)
2. Run `docker-compose build`
3. Run `docker-compose up`
4. Navigate to `localhost`


## Deployment

Deployment is fairly simple at the moment, just checkout the latest code and run:

```
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up
```
