
[![Build Status Widget]][Build Status] [![DockerHub Widget]][DockerHub]

# Description

Kompose UI is a web interface for [Kompose](http://kompose.io). It helps people easily switch from `docker-compose` to `Kubernetes` by converting the YAML files.

Here is a [live demo for the project](https://composetokube.com)

# Using kompose UI

You can either use the docker image from docker hub or run the project locally

## Use the Docker Image

* Pull the Image

```sh
docker pull jadcham/komposeui:latest
```

* Run the container
```sh
docker run -it --name komposeui -p 8000:8000 jadcham/komposeui
```

That's it ! Happy converting.

## Run the Project locally

* Install the requirements
```sh
pip install -r requirements.txt
```

* Install Kompose on your machine

[Check the Kompose Installation Guide](https://github.com/kubernetes/kompose#installation)

* Make sure kompose is properly installed
```sh
kompose version
```

* Prepare the database
```sh
python manage.py makemigrations
python manage.py migrate
```

* Run django
```sh
python manage.py runserver 0.0.0.0:8000
```

# Contributions and Support

__Issues:__ If you find an issue or want to suggest a feature [file an issue here](https://github.com/jadcham/komposeui/issues).

__Contributions:__ If you want to contribute to the project [make a pull request](https://github.com/jadcham/komposeui/pulls).


[Build Status]: https://travis-ci.org/jadcham/komposeui
[Build Status Widget]: https://travis-ci.org/jadcham/komposeui.svg?branch=master
[DockerHub]: https://hub.docker.com/r/jadcham/komposeui/
[DockerHub Widget]: https://img.shields.io/docker/pulls/jadcham/komposeui.svg

