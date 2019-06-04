Luizalabs Employee Management
=============================

[![Build Status](https://travis-ci.org/Charliiee/luizalabs-employee-management.svg?branch=master)](https://travis-ci.org/Charliiee/luizalabs-employee-management)

Contributing
------------

1. Clone repo:

```bash
$ git clone https://github.com/Charliiee/luizalabs-employee-management.git && cd luizalabs-employee-management
```

2. Create virtualenv:

```bash
$ python3 -m venv env
```

3. Activate virtualenv:

```bash
$ source env/bin/activate
```

4. Install dependencies:

```bash
$ pip install -r requirements.txt
```

5. Migrate database:

```bash
$ ./manage.py migrate
```

6. Create admin user:

```bash
$ ./manage.py createsuperuser --username admin --email admin@luizalabs.com.br
```

* Obs: You can replace both username and email to whatever you prefer

7. Run local server

```bash
$ ./manage.py runserver
```

##### Consuming API

Example with httpie:

```bash
$ http :8000/api/v1/employees/
```

##### Response:
```http
HTTP/1.1 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 173
Content-Type: application/json
Date: Tue, 04 Jun 2019 00:54:49 GMT
Server: WSGIServer/0.2 CPython/3.7.3
Vary: Accept, Cookie
X-Frame-Options: SAMEORIGIN

[
    {
        "department": "Marketing",
        "email": "jane.doe@luizalabs.com",
        "id": 2,
        "name": "Jane Doe"
    },
    {
        "department": "Development",
        "email": "john.doe@luizalabs.com",
        "id": 1,
        "name": "John Doe"
    }
]
```
