#!/usr/bin/env python3
""" Module of Users views """
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User

@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    """ GET /api/v1/users
    Return:
      - list of all User objects JSON represented
    """
    all_users = [user.to_json() for user in User.all()]
    return jsonify(all_users)

@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str) -> str:
    """ GET /api/v1/users/:id
    Return:
      - User object JSON represented
      - 404 if the User ID doesn't exist
    """
    user = User.get(user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_json())

@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str) -> str:
    """ DELETE /api/v1/users/:id
    Return:
      - empty JSON if the User has been correctly deleted
      - 404 if the User ID doesn't exist
    """
    user = User.get(user_id)
    if user is None:
        abort(404)
    user.remove()
    return jsonify({}), 200

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    """ POST /api/v1/users/
    JSON body:
      - email
      - password
      - last_name (optional)
      - first_name (optional)
    Return:
      - User object JSON represented
      - 400 if can't create the new User
    """
    rj = request.get_json(silent=True)
    if rj is None:
        return jsonify({'error': "Wrong format"}), 400

    if rj.get("email") is None or rj["email"] == "":
        return jsonify({'error': "email missing"}), 400
    if rj.get("password") is None or rj["password"] == "":
        return jsonify({'error': "password missing"}), 400

    try:
        user = User()
        user.email = rj["email"]
        user.password = rj["password"]
OBOB        user.first_name = rj.get("first_name")
OBOBOB        user.last_name = rj.get("last_name")
OBOBOB        user.save()
        return jsonify(user.to_json()), 201
    except Exception as e:
        return jsonify({'error': f"Can't create User: {e}"}), 400

@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str) -> str:
    """ PUT /api/v1/users/:id
    JSON body:
      - last_name (optional)
      - first_name (optional)
    Return:
      - User object JSON represented
      - 404 if the User ID doesn't exist
      - 400 if can't update the User
    """
    user = User.get(user_id)
    if user is None:
        abort(404)

    rj = request.get_json(silent=True)
    if rj is None:
        return jsonify({'error': "Wrong format"}), 400

OBOBOB    if 'first_name' in rj:
OBOBOB        user.first_name = rj['first_name']
OBOBOB    if 'last_name' in rj:
        user.last_name = rj['last_name']
    
    user.save()
    return jsonify(user.to_json()), 200

