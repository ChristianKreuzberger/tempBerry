# Temperature Monitor for Raspberry PI (TempBerry)

[![Build Status](https://travis-ci.org/ChristianKreuzberger/tempBerry.svg?branch=master)](https://travis-ci.org/ChristianKreuzberger/tempBerry)

This project contains the backend for the Raspberry PI Temperature monitor. It is written in Python (3.5+) and uses the
 following components/packages/libraries:
 
* Django 2.2 (powered by unicorns)
* Django Rest Framework 3.10 (provides a wonderful REST API)
* Whitenoise (for serving static files)
* gunicorn (running django)
* Redis / Django-Redis for some caching
* MySQL/Postgres as a database backend (Postgres is preferred though)

Please note that this project is work in progress, comes without warranty, and should definately only be used for
 experimenting and as a learning resource, but not for any production use. 

## Content

This repo contains the following pieces:

* a python script that collects temperatures from "any" source using pilight (see [receive.py](receive.py))
* a Django backend that allows collecting temperature data (see [app folder](app/))
* a docker-compose setup for development (see [docker-compose.yml](docker-compose.yml) and the [docker folder](docker/))
* a kubernetes setup for production deployments (see [deploy folder](deploy/))

There is also a rudimentary frontend application available at https://gitlab.com/ckreuzberger/tempberry-frontend. 

## Development Setup using Docker

To start development locally, build the docker images and run migrations

```bash
docker-compose build
docker-compose run --rm python python manage.py migrate
```

Consider adding a Django Superuser for the Django Admin Panel using
```bash
docker-compose run --rm python python manage.py createsuperuser
```

Finally, start it up using
```bash
docker-compose up
```
You should be able to access the backend using http://127.0.0.1:8000/, the API using http://127.0.0.1:8000/api/ and the
 Django Admin Panel using http://127.0.0.1:8000/admin/.

## Production Setup using Kubernetes

Deployment Files are in the [deploy/](deploy/) subfolder.

Make sure to add the **.env** file as follows:
(todo: this is not implemented yet...)
```bash
kubectl create configmap tempberry-backend-config --from-file=.env
```

Then apply the Kubernetes yaml files for the Postgres database using

```bash
kubectl apply -f deploy/postgres-storage.yaml
kubectl apply -f deploy/postgres-credentials.yaml
kubectl apply -f deploy/postgres.yaml
```

Verify that you can connect to the Postgres Server using

```bash
kubectl port-forward svc/postgres 5432:5432
```

Then apply the tempberry backend deployment yaml using

```bash
kubectl apply -f deploy/tempberry-backend.yaml
```

and also apply an ingress (this requires you to have a working ingress gateway, e.g. [nginx-ingress](https://kubernetes.github.io/ingress-nginx/deploy/)):

```bash
kubectl apply -f deploy/tempberry-backend-ingress.yaml
```

Once the pods are ready, run the migrations using

```bash
kubectl exec -it deployment/tempberry-backend python manage.py migrate
```

Finally, create a superuser using

```bash
kubectl exec -it deployment/tempberry-backend python manage.py createsuperuser
```

## License

The source code within this repository is made available using the MIT License. See [LICENSE](LICENSE).

## Contributions

As this is more of a hobby project for myself, I do not expect any contributions. Please do not expect any Pull 
 Requests to be merged (except for minor changes such as bugfixes or typo fixes).
