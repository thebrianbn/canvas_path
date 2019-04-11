# canvas_path
A web application used for course management in universities.

### Update database schema
```
python manage.py makemigrations
```

### Apply database schema
```
python manage.py migrate
```

### Insert all database instances
```
python database_insert.py
```

### Create admin account
```
python manage.py createsuperuser
email: admin@lionstate.edu
password: test12345
```

### Start the local host
```
python manage.py runserver
```