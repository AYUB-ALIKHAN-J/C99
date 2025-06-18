from flask import Blueprint, request, jsonify

def create_search_controller(search_service):
    bp = Blueprint('search', __name__)

    @bp.route('/services/search', methods=['GET'])
    def search_services():
        query = request.args.get('q', '')
        results = search_service.search(query)
        return jsonify(results), 200

    return bp
