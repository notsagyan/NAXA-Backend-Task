# Backend Task Overview

## Getting Started

First clone the repository from Github and switch to the new directory :

```
git@github.com:notsagyan/NAXA-Backend-Task.git
```

Create a new virtual environment for the project and activate it. (*Python 3.11.4*) :

```
conda create --name naxa_env 
conda install python=3.11.4
```

Install project dependencies :

```
pip install -r requirements.txt
```

Apply migrations :

```
python manage.py makemigrations
python manage.py migrate
```

Make a new .env file with the following variables and configure them:

```

```

Run the project :

```
python manage.py runserver
```

Run celery worker and beat:

```
celery -A backend_task worker -l info
celery -A backend task beat -l info
```

Running tests :

```
EXPORT DJANGO_SETTINGS_MODULE=backend_task.settings 
SET DJANGO_SETTIGNS_MODULE=backend_task.settings (Windows)
pytest apps/authentication/tests.py
```

## Overview

The project is entitled backend task.

I have switched the username field with the email address as the field required for login and register as it makes more sense. Extended the user model with AbstractBaseUser for this purpose and to add certain fields.

No authentication methods were specified, so I decided to go with JWT Authentication as it is secured, widely-used and adheres to the RESTful principle. I have created an API for signup but for the login the following APIs should be used for getting access and refresh tokens.

```
/api/token/
/api/token/refresh/
```

Integrated postGIS and geoDjango for processing and saving coordinates.

Integrated celery for scheduled task to wish users on their birthday.
