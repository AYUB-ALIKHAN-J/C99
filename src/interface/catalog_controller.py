from flask import Blueprint, request, jsonify

def create_catalog_controller(catalog_service):
    bp = Blueprint('catalog', __name__)

    @bp.route('/services', methods=['GET'])
    def list_services():
        services = catalog_service.list_services()
        for s in services:
            s['_id'] = str(s['_id'])  # Convert ObjectId to string for JSON
        return jsonify(services), 200

    @bp.route('/services/<service_id>', methods=['GET'])
    def service_details(service_id):
        service = catalog_service.get_service_details(service_id)
        if not service:
            return jsonify({"error": "Service not found", "code": "NOT_FOUND"}), 404
        service['_id'] = str(service['_id'])
        return jsonify(service), 200

    @bp.route('/services/filter', methods=['POST'])
    def filter_services():
        filters = request.json
        services = catalog_service.filter_services(filters)
        for s in services:
            s['_id'] = str(s['_id'])
        return jsonify(services), 200

    return bp
