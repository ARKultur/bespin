# Bespin

---

## 💻 project description

This services stores and manages [ARKultur](https://arkultur.creative-rift.com)'s models, in accordance with the
[GeoJSON](https://www.rfc-editor.org/rfc/rfc7946) format.

### 🏭 Tech stack

- [DRF](https://www.django-rest-framework.org/) is the main framework used to build the API
- [Postgres](https://www.postgresql.org/) is the database used for this project
- [Docker](https://www.docker.com/) is used to serve and deploy the application through containers (we use `docker-compose` to orchestrate them seemlessly)
- [Gunicorn](https://gunicorn.org/) is our WSGI of choice, to serve HTTP requests across multiple workers.

---

## 📐 project setup

### ✨ As project contributor

If you want to run locally the application, you should first run the `setup` scripts,
and then run it as you would normally for a Python.

> Note: it is recommanded to use [ASDF](https://asdf-vm.com/guide/getting-started.html) to ensure maximum compatibility.
> In our case, we use it to specify the Python version, which is currently `3.10.8`

Install setup:

<details>

```bash

# go to the project root directory
cd Bespin

# run the database setup script:
# - will assume you're running Ubuntu for the postgresql installation etc
# - will automatically install packages, such as Postgresql 15.
#
# [!] if you have another install running on port 5432, it could create conflicts!
./scripts/setup.sh

# create a virtual env
python -m venv ~/.local/venv_bespin

# enable the virtual env
. ~/.local/venv_lunit/bin/activate

# install pip dependencies
pip install -r requirements.txt

# migrations should already be done, so you can just run the server
python manage.py runserver 8080

# if you need to create new migrations (make sure postgresql is running and you have your env values set up)
python manage.py makemigrations
python manage.py migrate

# or, if you wish to interact with the models directly:
python manage.py shell
```

</details>

### ✨ As a project user

If you're just planning on _using_ the API, but not develop on it, you can easily run it with Docker.

1. Install [Docker](https://docs.docker.com/engine/install/ubuntu/) if not already done

2. [Optional] Do the [post-install steps](https://docs.docker.com/engine/install/linux-postinstall/)

3. Run the following, once you have tested that your install works:

<details>

```bash

# build the image
docker build . -t bespin

# run on port 8080 (assuming postgresql daemon is running and migrations have been done)
docker run -p "8080:8080" bespin

```

</details>

---

## 🎖 Features

### 🧑 Authentication

Authentication is done by providing your email and password.
You then get a `Token` you can use as a `Bearer <Token>` in the `Authorization` field of your requests.

<details>

#### Support for 2FA

-> Three methods should be supported by this project:
 - [x] Authenticator app
 - [x] Email 2FA
 - [x] Phone number 2FA

</details>

### 🚩 Domain endpoints


### 🧪 Testing

To run tests, just do
```bash
# enable virtualenv
. ~/.local/venv_bespin/bin/activate

# assuming postgresql service is already running in the background
python manage.py test

# or, if you want to test a single test case
python manage.py test api.tests.AuthTestCase

# or, just one method
python manage.py test api.tests.AuthTestCase.test_can_login_customer_account
```

---

## 🔍 Usage

You may find an [OpenAPI](https://www.openapis.org/) specification at the `/docs` endpoint.
This can then be important in the REST client of your choice, we recommend:
- [Postman](https://www.postman.com/) -- industry leader, full of features, and great for development within a team.
- [Insomnia](https://insomnia.rest/) -- works offline, comfy UI, super easy to work with.
- [HTTPie](https://httpie.io/docs/cli) -- works in the Terminal, but currently cannot import OpenAPI specs.

---
