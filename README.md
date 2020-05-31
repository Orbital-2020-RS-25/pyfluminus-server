# Python Luminus Server

Flask server to call APIs from [pyfluminus](https://github.com/raynoldng/pyfluminus). 

Please refer to the [API documentation](https://app.swaggerhub.com/apis-docs/orbital-rs25/another-luminus/v3) for usage. 

Currently hosted on Heroku. 

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