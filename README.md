# Python Luminus Server

Flask server to call APIs from [pyfluminus](https://github.com/raynoldng/pyfluminus). 

To create database locally: 
```
flask db migrate
flask db upgrade
```

To start locally: 
```
export FLASK_APP=server.py
export FLASK_ENV=development
* to run in debug mode
flask run
```