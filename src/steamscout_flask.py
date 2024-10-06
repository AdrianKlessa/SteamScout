from flask import Flask, request, jsonify, abort
import search_manager

app = Flask(__name__)

@app.route('/get-games-by-name', methods=['GET'])
def find_games_by_name():
    request_json = request.get_json()
    game_name = request_json.get('game_name')
    if not game_name:
        abort(400)
    res = search_manager.game_search(game_name)
    return jsonify(res)

@app.route('/get-games-by-similarity', methods=['GET'])
def find_similar_games():
    request_json = request.get_json()
    game_name = request_json.get('game_name')
    app_id = request_json.get("app_id")
    if not app_id:
        if not game_name:
            abort(400)
        app_id = search_manager.get_game_app_id_from_title(game_name)
    if app_id==-1:
        abort(404)
    include_tag = request_json.get('include_tag')
    exclude_tag = request_json.get('exclude_tag')
    adult_content_filter = request_json.get("adult_content_filter")
    max_reviews = request_json.get('max_reviews')
    res = search_manager.find_similar_games(app_id, exclude_tag, include_tag, adult_content_filter, max_reviews)
    return jsonify([x.serialize() for x in res])

"""
if __name__ == '__main__':
    app.run(debug=True)
"""