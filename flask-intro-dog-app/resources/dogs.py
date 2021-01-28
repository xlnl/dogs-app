# similar to controllers
import models

from flask import Blueprint, jsonify, request
# peewee thing to convert model to dictionary 
from playhouse.shortcuts import model_to_dict

# first argument is blueprints name
# second argument is its import_name
# The third argument is the url_prefix so we don't have to prefix all our apis with /api/v1
dog = Blueprint('dogs', 'dog')

# Here we are defining out route, as a "GET" route

# We are using peewee's .select() method to find all the dogs, on our Dog Model.

# model_to_dict(dog) - is a function that will change our Model object (dog) to a Dictionary class, - We have to do this because we cannot jsonify something from a "Model" class, so in order to respond to the client we must change our datatype from a Model Class to a Dictionary Class instance.
@dog.route('/', methods=["GET"])
def get_all_dogs():
    ## find the dogs and change each one to a dictionary into a new array
    try:
        # query the DB to get all the dogs
        all_dogs = models.Dog.select()
        # parse the models into dictionary
        dogs_to_dict = [model_to_dict(dog) for dog in all_dogs]
        # shorter way => dogs = [model_to_dict(dog) for dog in models.Dog.select()]
        return jsonify(
            data=dogs_to_dict, 
            status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(
            data={}, 
            status={"code": 401, "message": "Error getting the resources"})

# Here we are using peewee's create method on our model object to create an entry into our database.

# payload = request.get_json() - in this line we are using the global request object we just talked about in the above, to "get_json" from the request, so that is the object that we will send over from the client!

# What doess **payload mean?
# It's what is called a spread operator, basically what that means is we can take the properties of an object and "spread them out into the method call. So for example, if we sent over an object like this.
#  dog = models.Dog.create(name=payload['owner'], owner=payload["owner"], breed=payload["breed"])

# @dog.route('/', methods=["POST"])
# def create_dogs():
#     ## see request payload anagolous to req.body in express
#     payload = request.get_json()
#     dog = models.Dog.create(**payload)
#     ## see the object
#     # print(dog.__dict__)
#     ## Look at all the methods
#     # print(dir(dog))
#     # Change the model to a dict
#     # print(model_to_dict(dog), 'model to dict')
#     dog_dict = model_to_dict(dog)
#     return jsonify(
#         data=dog_dict, 
#         status={"code": 201, "message": "Success"})

@dog.route('/<dog_id>', methods=["GET"])
def get_dog(dog_id):
    try:
        dog = models.Dog.get_by_id(dog_id)
        dog_dict = model_to_dict(dog)
        return jsonify(
            data=dog_dict, 
            status={"code": 201, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(
            data={}, 
            status={"code": 401, "message": "Error getting the resources"})

@dog.route('/<dog_id>/update', methods=["PUT"])
def update_dog(dog_id):
    try:
        payload = request.get_json()
        query = models.Dog.update(**payload).where(models.Dog.id==dog_id)
        query.execute()
        updated_dog = model_to_dict(models.Dog.get_by_id(dog_id))
        return jsonify(
            data=updated_dog, 
            status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(
            data={}, 
            status={"code": 401, "message": "Error getting the resources"})

@dog.route('/<dog_id>', methods=["Delete"])
def delete_dog(dog_id):
    try:
        dog_to_delete = models.Dog.get_by_id(dog_id)
        dog_to_delete.delete_instance()
        return jsonify(
            data={}, 
            status={"code": 200, "message": "Success, resources successfully delete"})
    except models.DoesNotExist:
        return jsonify(
            data={}, 
            status={"code": 401, "message": "Error getting the resources"})