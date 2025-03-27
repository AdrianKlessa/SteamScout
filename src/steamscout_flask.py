from functools import wraps

import argon2.exceptions
import jwt
from flask import Flask, request, jsonify, abort, make_response
import search_manager
import os
from sqlite_manager import get_user_by_username
from argon2 import PasswordHasher

app = Flask(__name__)
JWT_SECRET = os.getenv('JWT_SECRET')
ph = PasswordHasher()

def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response

def verify_user(username: str, password: str)->bool:
    actual_user = get_user_by_username(username)
    if actual_user is None:
        return False
    try:
        ph.verify(actual_user.password_hash, password)
        return True
    except argon2.exceptions.VerifyMismatchError:
        return False

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get("Authorization")
        if auth_header and len(auth_header.split()) == 2:
            token = auth_header.split()[1]
        if not token:
            return jsonify({'message': 'A JWT token is required to view this'}), 401
        try:
            data = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        except Exception as e:
            print(e)
            return jsonify({'message': 'Invalid JWT token'}), 403

        return func(*args, **kwargs)

    return decorated

@app.after_request
def after_request_cors(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/get-games-by-name', methods=['GET', 'OPTIONS'])
@token_required
def find_games_by_name():
    if request.method == "OPTIONS": # CORS preflight
        return _build_cors_preflight_response()
    game_name = request.args.get('game_name')
    if not game_name:
        abort(400)
    results = search_manager.game_search(game_name)
    response = jsonify(results)
    return response

@app.route('/get-games-by-similarity', methods=['GET', 'OPTIONS'])
@token_required
def find_similar_games():
    if request.method == "OPTIONS": # CORS preflight
        return _build_cors_preflight_response()
    game_name = request.args.get('game_name')
    app_id = request.args.get("app_id")
    if not app_id:
        if not game_name:
            abort(400)
        app_id = search_manager.get_game_app_id_from_title(game_name)
    if app_id==-1:
        abort(404)
    include_tag = request.args.get('include_tag')
    exclude_tag = request.args.get('exclude_tag')
    adult_content_filter = request.args.get("adult_content_filter")
    max_reviews = request.args.get('max_reviews')
    results = search_manager.find_similar_games(app_id, exclude_tag, include_tag, adult_content_filter, max_reviews)
    response = jsonify([x.serialize() for x in results])
    return response

@app.route('/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    username = request.json.get('username')
    password = request.json.get('password')
    if not username or not password:
        abort(400)
    if not verify_user(username, password):
        abort(401)
    encoded = jwt.encode({'username': username}, JWT_SECRET)
    return jsonify({'token': encoded})

if __name__ == '__main__':
    app.run(debug=True)
