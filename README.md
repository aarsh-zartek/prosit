# Prosit

This repository contains the backend code for Prosit


## Technology Stack

> Python -> 3.10.2

> Django -> 4.0.1

> DRF -> 3.13.3

## Installation & Setup

### Create a new virtualenv and activate it

Create a new virtualenv
> python -m venv `<virtual-env>`

Activate the virtualenv
> source `path/to/virtual-env/bin/activate`

### Install required packages from `requirements.txt`

> pip install -r requirements.txt

### Environment Variables

Create `.env` file in `prosit` directory

.env.example file is provided for reference in `prosit`

### Logs

Create `logs` directory & `prosit.log` file inside it.

### Setting Up the Database

Making migrations

> python manage.py makemigrations

Migrate

> python manage.py migrate

