# How to run

```shell

docker-compose stop; \
  docker-compose rm -vf; \
  docker-compose build base; \
  docker-compose build; \
  docker-compose up -d; \
  sleep 10; \
  docker-compose logs
```