# TempBerry - Temperature Monitor for Raspberry PI

[![Build Status](https://travis-ci.com/ChristianKreuzberger/tempBerry.svg?branch=master)](https://travis-ci.com/ChristianKreuzberger/tempBerry)

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

## Production Setup using SystemD

This requires Python 3.5 and virtualenv to be pre-installed on your system.

1. Create a new virtualenv for python 3.5 and activate it
1. Install requirements using `pip install -r requirements.txt`
1. Run migrations, create superuser, etc...
1. Copy `.env.example` to a `.env` file and edit the values according to your setup
1. Set up a systemd service unit with the following content
    ```
    [Unit]
    Requires=tempberry_gunicorn.socket
    Description=gunicorn daemon for tempberry
    After=network.target
     
    [Service]
    # make sure a runtime directory is accessible from the outside
    RuntimeDirectoryMode=0775
    PIDFile=%h/.%p.pid
    # define working directory (%h = home directory)
    WorkingDirectory=%h/tempberry/app
    Environment="DJANGO_SETTINGS_MODULE=tempBerry.settings.live"
    EnvironmentFile=%h/tempberry/.env
    ExecStart=%h/tempberry/venv/bin/gunicorn --pid %h/.%p.pid --workers 4 --log-level debug --bind 127.0.1.1:5001 tempBerry.wsgi 
    ExecReload=/bin/kill -s HUP $MAINPID
    ExecStop=/bin/kill -s TERM $MAINPID
    
    
    # security hardening
    # see https://gist.github.com/ageis/f5595e59b1cddb1513d1b425a323db04
    # make sure the following permissions are only applied for ExecStart, but not for ExecReload/ExecStop
    PermissionsStartOnly=True
    
    NoNewPrivileges=yes
    PrivateTmp=yes
    ProtectSystem=strict
    ProtectControlGroups=yes
    RestrictAddressFamilies=AF_UNIX AF_INET AF_INET6 AF_NETLINK
    RestrictRealtime=yes
    RestrictNamespaces=yes
    MemoryDenyWriteExecute=yes
    
    # disabled as they cause issues with gunicorn
    #PrivateDevices=yes
    #DevicePolicy=closed
     
    [Install]
    WantedBy=multi-user.target
    ```
1. Set up a systemd socket unit:
    ```
    [Unit]
    Description=gunicorn socket for tempberry
     
    [Socket]
    ListenStream=127.0.1.1:5001
     
    [Install]
    WantedBy=sockets.target
    ```

Enable the socket and the service, and start the socket. Accesing the socket (using port 5001) should automatically 
start the service.


## License

The source code within this repository is made available using the MIT License. See [LICENSE](LICENSE).

## Contributions

As this is more of a hobby project for myself, I do not expect any contributions. Please do not expect any Pull 
 Requests to be merged (except for minor changes such as bugfixes or typo fixes).
