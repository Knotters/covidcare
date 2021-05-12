# Covid Help

## Setup

### Environment

Copy contents of [covid/.env.example](covid/.env.example) to a new file at [covid/.env](covid/.env), and set the values in content accordingly.

### Dependencies

```bash
pip install -r requirements.txt
```

or similar command depending on your system platform.

### DB setup

```bash
py manage.py makemigrations
```

```bash
py manage.py migrate
```

### Server

```bash
python manage.py runserver 5000
```

or similar command depending on your system platform.
