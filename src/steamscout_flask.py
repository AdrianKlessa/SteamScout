from flask import Flask, request, jsonify, abort, make_response
import search_manager

app = Flask(__name__)

def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response

@app.after_request
def after_request_cors(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/get-games-by-name', methods=['GET', 'OPTIONS'])
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


if __name__ == '__main__':
    app.run(debug=True)
