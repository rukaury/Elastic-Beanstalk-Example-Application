# Elastic Beanstalk Example Deployment Application <img src="https://upload.wikimedia.org/wikipedia/commons/9/93/Amazon_Web_Services_Logo.svg" width="50px" height="50px"/>

This is an example application you can use to deploy on elastic beanstalk. This example app is built on the work of [Sam Louden's](https://github.com/orgs/DIS-SIN/people/deepklim) [Data Explorer](https://github.com/DIS-SIN/CSPS-Data-Explorer). 

## Tech Stack

### Backend

Flask: A python microframwork for backend web applications
MySQL v8.*: Relational database

### Frontend

Javascript, HTML, CSS and jQuery

## Configuration

### Environment Variables

```BASIC_AUTH_USERNAME```: The username for HTTP Basic Auth

```BASIC_AUTH_PASSWORD```: The password for HTTP Basic Auth

```DB_HOST```: The MySQL host server *PROD ONLY*

```DB_USER```: The MySQL user

```DB_PASSWORD```: The MySQL user's password

```DB_DATABASE_NAME```: The name of the MySQL Database

```SECRET_KEY```: The application secret key

```GOOGLE_MAPS_API_KEY```: As the name implies

### Setting up the database

A CLI utility has been provided for convenience. You must first initialise the flask cli by providing the FLASK_APP environment variable 

```sh
$ cd ./data_explorer
$ export FLASK_APP=.
```
To test if this works call the flask command

```bash
$ flask
```
The following output should appear

```
Usage: flask [OPTIONS] COMMAND [ARGS]...

  A general utility script for Flask applications.

  Provides commands from Flask, extensions, and the application. Loads the
  application defined in the FLASK_APP environment variable, or from a
  wsgi.py file. Setting the FLASK_ENV environment variable to 'development'
  will enable debug mode.

    $ export FLASK_APP=hello.py
    $ export FLASK_ENV=development
    $ flask run

Options:
  --version  Show the flask version
  --help     Show this message and exit.

Commands:
  init-db  Set up mysql database.
  routes   Show the routes for the app.
  run      Runs a development server.
  shell    Runs a shell in the app context.
```

#### Setting up your local development database

First set the needed environment variables ```DB_USER``` and ```DB_PASSWORD```

```sh
$ export DB_USER=user
$ export DB_PASSWORD=password
```
Then call the CLI command with the --local switch

```sh
flask init-db --local
```
The following output should appear

```
Creating table 1 of 5: comments
Creating table 2 of 5: lsr_last_year
Creating table 3 of 5: lsr_this_year
Creating table 4 of 5: product_info
Creating table 5 of 5: ratings
```

#### Setting up production database

Do the same steps as local except also export the ```DB_HOST``` environment variable and drop the --local switch from the command

## Starting the application

The production and development switch is located in the ```data_explorer/config.py``` folder

Set DEBUG = True for development and DEBUG = False for production 

``` Python
class Config:
    # DEBUG=True (Dev) DEBUG=False (Prod)
    DEBUG = False
    LOCAL_DB = False
    LAST_YEAR = '2018-19'
    THIS_YEAR = '2019-20'
    BABEL_DEFAULT_LOCALE = 'en'
    # Options for flask.jsonify
    JSON_AS_ASCII = False
    JSONIFY_PRETTYPRINT_REGULAR = True
    JSON_SORT_KEYS = False
    # Load strings from environ vars to avoid storing in plaintext
    BASIC_AUTH_USERNAME = os.environ.get("BASIC_AUTH_USERNAME")
    BASIC_AUTH_PASSWORD = os.environ.get("BASIC_AUTH_PASSWORD")
    SECRET_KEY = os.environ.get('SECRET_KEY')
    GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')
```

Then call in the root folder

```sh
$ python application.py
```

You should see

```
 * Serving Flask app "data_explorer" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```