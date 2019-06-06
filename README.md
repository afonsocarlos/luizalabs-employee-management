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

#### Consuming API

##### Example with httpie:

First get a jwt token:
```bash
$ http :8000/api-token-auth/ username=username password=pass
```

Response:
```http
HTTP/1.1 200 OK
Allow: POST, OPTIONS
Content-Length: 232
Content-Type: application/json
Date: Wed, 05 Jun 2019 02:18:49 GMT
Server: WSGIServer/0.2 CPython/3.7.3
Vary: Accept
X-Frame-Options: SAMEORIGIN

{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNTU5NzAxNDI5LCJlbWFpbCI6ImFkbWluQGx1aXphbGFicy5jb20uYnIiLCJvcmlnX2lhdCI6MTU1OTcwMTEyOX0.X0zaJ_ZimtBEUMHpNVtr8uQrdYakKFcoImvOr4_Bjh4"
}
```

Then make request
```bash
$ http :8000/api/v1/employees/ "Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNTU5NzAxNDI5LCJlbWFpbCI6ImFkbWluQGx1aXphbGFicy5jb20uYnIiLCJvcmlnX2lhdCI6MTU1OTcwMTEyOX0.X0zaJ_ZimtBEUMHpNVtr8uQrdYakKFcoImvOr4_Bjh4"
```

Response:
```http
HTTP/1.1 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 173
Content-Type: application/json
Date: Tue, 04 Jun 2019 00:54:49 GMT
Server: WSGIServer/0.2 CPython/3.7.3
Vary: Accept, Cookie
X-Frame-Options: SAMEORIGIN

{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "birthdate": "1998-03-11",
            "department": "Marketing",
            "email": "jane.doe@luizalabs.com",
            "gender": "F",
            "hire_date": "2017-05-26",
            "id": 2,
            "name": "Jane Doe"
        },
        {
            "birthdate": "1989-08-05",
            "department": "Development",
            "email": "john.doe@luizalabs.com",
            "gender": "M",
            "hire_date": "2010-11-18",
            "id": 1,
            "name": "John Doe"
        },
    ]
}
```

For more information about API endpoints access API documentation at localhost:8000/docs/
