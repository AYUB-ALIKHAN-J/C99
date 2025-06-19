from flask import Blueprint, request, jsonify
from typing import Dict, Any, List
from .utils import format_response # Import utility functions

def create_search_controller(search_service):
    bp = Blueprint('search', __name__)

    @bp.route('/services/search', methods=['GET'])
    def search_services():
        query = request.args.get('q', '')
        results = search_service.search(query)
        return jsonify(format_response(results)), 200

    return bp
