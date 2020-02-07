#
# Memento
# Backend
# Flask App
#

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_sockets import Sockets
from healthcheck import HealthCheck

from . import config

# app core componments
app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
cors = CORS(app)
sockets = Sockets(app)
# configure healthcheck route
health = HealthCheck(app, "/healthz")

# register api components
from .api import register_api
register_api(app, sockets)

## basic routes
# root route - backend status
@app.route('/')
def route_status():
    return f"Memento Backend - API v{config.API_VERSION} is up and running!"

## health checks
# check database connectivity
@health.add_check
def check_database():
    # try to execute a simple query on database
    is_database_ok = True
    message = "database ok"
    try:
        db.session.execute("SELECT 1")
    except Exception as e:
        message = str(e)
        is_database_ok = False
    return is_database_ok, message


# return db connection to pool
# required to prevent the connection pool from 
# running out of connnections and causing timeouts
@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()
