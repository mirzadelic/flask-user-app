# User app in Flask
User app in Flask with signup, login and user crud.

Used:
* flask
* sqlalchemy

## Features
* signup
* login
* user crud

## Usage

### Signup
* url: `/api/signup/`
  request params: `first_name`, `last_name`, `email`, `password`
  response: `user object`
### Login
* url: `/api/login/`
  request params: `email`, `password`
  response: `token`, `user object`
### User CRUD
* url: `/api/users/`
  methods: `GET`, `POST`
* url: `/api/users/<user_id>/`
  methods: `GET`, `PUT`

Use `token` in every request as `Authorization` header:
```
Authorization: JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2NsYWltcyI6e30sImp0aSI6IjQ1OGU2aBzG1K7s
```

## Install
```
virtualenv flask-user-app
source flask-user-app/bin/activate
pip install -r requirements.txt
```

## Run:
```
python app/app.py
```

## Examples:
Signup:
```
curl -H "Content-Type: application/json" -X POST -d '{"email": "test@test.com", "first_name": "Test", "last_name": "Test", "password": "test"}' http://localhost:5000/api/signup/
```
Login:
```
curl -H "Content-Type: application/json" -X POST -d '{"email":"test@test.com","password":"test"}' http://localhost:5000/api/login/
```
List users:
```
curl -H "Content-Type: application/json" -H "Authorization: JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2NsYWltcyI6e30sImp0aSI6IjQ1OGU2aBzG1K7s" http://localhost:5000/api/users/
```

