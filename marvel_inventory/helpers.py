from functools import wraps

import secrets
from flask import request, jsonify, json

from marvel_inventory.models import User

import decimal

from marvel import Marvel

def APIMarvel(name):   
    marvel = Marvel(PUBLIC_KEY = "d04361fb613e941e150ff9c6b928b1b4", PRIVATE_KEY = "42be969884a8c719cfbc8f4479895d2189a3697e" )
    characters = marvel.characters
    my_char = characters.all(name=name)["data"]["results"]
    return my_char




def token_required(our_flask_function):
    @wraps(our_flask_function)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token'].split(' ')[1]
            print(token)

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            our_user = User.query.filter_by(token = token).first()
            print(our_user)
            if not our_user or our_user.token != token:
                return jsonify({'message': 'Token is invalid'})

        except:
            owner = User.query.filter_by(token=token).first()
            if token != owner.token and secrets.compare_digest(token, owner.token):
                return jsonify({"message": "Token is invalid"})
        return our_flask_function(our_user, *args, **kwargs)
    return decorated

    


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return super(JSONEncoder, self).default(obj)



