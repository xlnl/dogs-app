from flask import Flask, render_template, g
# or just do "from flask import *" to grab all ^
from flask_cors import CORS
from flask_login import LoginManager

import models
from resources.dogs import dog
from resources.user_dogs import user_dogs
from resources.users import users

DEBUG = True
PORT = 8000

# Initialize an instance of the Flask class.
# This starts the website!
app = Flask(__name__)

app.config.from_pyfile('config.py')

############ vv "MIDDLEWARE" METHODS vv ##############

login_manager = LoginManager() # instantiating a new LoginManager in an app 
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    try:
        return models.User.get_by_id(user_id)
    except models.DoesNotExist:
        return None

# middleware as concept -> flask way to connect db before request & close db after each request
# """Connect to the database before each request."""
@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.connect()

# """Close the database connection after each request."""
@app.after_request
def after_request(response):
    g.db = models.DATABASE
    g.db.close()
    return response

CORS(dog, origins=['http://localhost:3000'], supports_credentials=True) 

app.register_blueprint(dog, url_prefix='/api/v1/dogs')
app.register_blueprint(user_dogs, url_prefix='/api/v1/user_dogs')
app.register_blueprint(users, url_prefix='/api/v1/users')
# express equivalent = app.use('/api/v1/dogs')

############ vv ROUTES vv ##############

# if you don't specify, it will assume that your route is a get request unless you want a route that's !GET like: 
#  @app.route('/', method=['POST'])

# The default URL ends in / ("my-website.com/").
# Return type must be a string, dict, tuple, etc but not an int
@app.route('/')
def index():
    return 'hi!'

# # returns a json object based on the key-values
# @app.route('/json')
# def dog():
#     return jsonify(name="Frankie", age=8)

# # more complicated json object testing
# @app.route('/sayhi')
# def say_hi():
#     return jsonify(msg='Hello', status=200, list=['bob', 'ricky'], artist='fatima')

# # returns the defined variable based on what's inputed within the arrows 
# @app.route('/sayhi/<username>')
# def hello(username):
#     # set params in python
#     return "Hello {}".format(username)

# combining it all! -> make sure to pass the variable through the function
# URL path format: http://localhost:8000/sayhello/lam?bandname=hewwogorls
# @app.route('/sayhello/<name>')
# # get and use params    ----> handles params
# def say_hello(name):
#     # get query string with <name>
#     # get the bandname query string from URL path as a branch --> handles query string
#     band = request.args.get('bandname')
#     # return the value to the end point
#     return jsonify(
#         msg='Hello', 
#         band_name=band, 
#         status=200, 
#         list=['bob', 'ricky'], 
#         artist='fatima ' + name)

# Run the app when the program starts!
# Invoking db method with "models.initialize()"
if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)