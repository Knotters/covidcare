# Covid Care

Covid pandemic related help resources for people in need.

## Setup

Built & Tested on Python v3.9.
Other dependencies and their respective versions are defined in [requirements.txt](requirements.txt).

### Prerequisites

- Mongo DB local server OR Mongo DB atlas cluster url.
- Python v3.x

### Environment

Copy the contents of [covid/.env.example](covid/.env.example) to a new file at [covid/.env](covid/.env), and set the values in content accordingly. Some values are provided by default.

### Dependencies

```bash
pip install -r requirements.txt
```

or similar command depending on your system platform.

### DB setup

Although we use mongoDB as our database server, the following commands are recommended to run for the first time, to not to leave any stones unturned.

```bash
py manage.py makemigrations
```

```bash
py manage.py migrate
```

or similar command(s) depending on your system platform.

### Server

```bash
python manage.py runserver 5000
```

or similar command depending on your system platform.

## Testing

Test files are located in folder of each application in this django project.

```bash
py manage.py test
```

