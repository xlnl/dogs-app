import models

from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict

user_dogs = Blueprint("user_dogs", "user_dogs")

@user_dogs.routes('/', methods=["POST"] )
def create_dogs():
    if current_user.id:
        payload = request.get_json()
        dog = models.Dog.create(**payload)
        dog_dict = model_to_dict(dog)

        # breakpoint()

        # create the relationship b/w dog and user
        user_dog_data = {
            "user": current_user.id,
            "dog": dog.id
        }

        models.UserDog.create(**user_dog_data)
        return jsonify(
            data=dog_dict, 
            status={"code": 201, "message": "Success"})