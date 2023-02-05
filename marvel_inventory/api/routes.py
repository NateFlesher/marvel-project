from flask import Blueprint, request, jsonify
from marvel_inventory.helpers import token_required
from marvel_inventory.models import db, Hero, hero_schema, heroes_schema

api = Blueprint('api', __name__, url_prefix = '/api')


@api.route('/getdata')
@token_required
def getdata(our_user):
    return {'some': 'value'}


#Generate Hero endpoint



#retreive all hero endpoints
@api.route('/heroes', methods = ['GET'])
@token_required
def get_heroes(our_user):
    owner = our_user.token
    heroes = Hero.query.filter_by(user_token = owner).all()
    response = heroes_schema.dump(heroes)

    return jsonify(response)


#retreive one hero endpoint
@api.route('/heroes/<id>', methods = ['GET'])
@token_required
def get_hero(our_user, id):
    owner = our_user.token
    if owner == our_user.token:
        hero = Hero.query.get(id)
        response = hero_schema.dump(hero)
        return jsonify(response)
    else:
        return jsonify({'message': 'Valid ID Required'}), 401



#delete hero endpoint
@api.route('/heroes/<id>', methods = ['DELETE'])
@token_required
def delete_heroes(our_user, id):
    hero = Hero.query.get(id)
    db.session.delete(hero)
    db.session.commit()

    response = hero_schema.dump(hero)
    return jsonify(response)