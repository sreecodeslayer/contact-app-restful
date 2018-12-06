# Contacts App Restful

### Running
1. Clone the repo : 
```bash
$ git clone https://gitlab.com/sreecodeslayer/contact-app-restful.git
$ cd contact-app-restful
```
2. Create databases : `contacts` and `contacts_test` in postgres
```psql
psql> CREATE DATABASE contacts;
psql> CREATE DATABASE contacts_test;
```
3. Install requirements in a virtual env of Python 3.6+
```bash
$ pip install -r requirements.txt
$ pip install -e .
```  
Optionally to run tests, install Pytest as well
```bash
$ pip install pytest
```
4. Run migrations
```bash
$ export CONTACTS_ENV=dev
$ export FLASK_APP=run.py
$ flask db init
$ flask db migrate
$ flask db upgrade
```
5. Optionally run tests
```bash
$ pytest
```
6. Running API via gunicorn
```bash
$ pip install gunicorn
$ gunicorn run:application -w 4
```

Configurations regarding Postgres Connection is inside `contacts/config.py` and can be configured as per the needs. Currently the app will try to connect with `postgres:postgres` to `locahost`

### Testing
1. Testing covers unit tests for User model and Records model (contacts table)
2. Testing also covers different aspects of API integration with the models like the Login/Signup cases, Auth based API requests for CRUD of contacts.