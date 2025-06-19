from flask import Blueprint, request, jsonify
from typing import Optional, Dict, Any, List
from .utils import format_response, format_error_response, convert_objectid # Import utility functions
import logging

def create_catalog_controller(catalog_service):
    bp = Blueprint('catalog', __name__)

    @bp.route('/services', methods=['GET'])
    def list_services():
        logging.info("Received request: LIST services with args: %s", dict(request.args))
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('pageSize', 20))
        skip = (page - 1) * page_size
        
        # Collect filters from request arguments, excluding pagination params
        filters = {k: v for k, v in request.args.items() if k not in ['page', 'pageSize', 'sort_by', 'sort_order']}
        
        # Handle specific filter types if needed (e.g., convert 'true'/'false' strings to bools)
        # Example: filters['is_on_sale'] = request.args.get('is_on_sale', type=lambda x: x.lower() == 'true')
        
        # Handle sorting
        sort_by = request.args.get('sort_by')
        sort_order = request.args.get('sort_order', 'asc') # 'asc' or 'desc'
        sort_param = None
        if sort_by:
            from pymongo import ASCENDING, DESCENDING # Import here to avoid circular dependency if placed at top
            sort_direction = ASCENDING if sort_order.lower() == 'asc' else DESCENDING
            sort_param = [(sort_by, sort_direction)]

        services = catalog_service.list_services(filters, skip, page_size, sort_param)
        
        # Pagination metadata (you might fetch total count from repo for more accuracy)
        total_services = len(services) # This would ideally come from a separate count query in repo
        pagination_info = {
            "page": page,
            "pageSize": page_size,
            "total_items": total_services,
            "total_pages": (total_services + page_size - 1) // page_size
        }
        
        return jsonify(format_response(services, pagination_info)), 200

    @bp.route('/services/<service_id>', methods=['GET'])
    def service_details(service_id):
        logging.info("Received request: GET service details for ID: %s", service_id)
        service = catalog_service.get_service_details(service_id)
        if not service:
            return jsonify(format_error_response("Service not found", "NOT_FOUND", 404)), 404
        
        return jsonify(format_response(service)), 200

    @bp.route('/services', methods=['POST'])
    def create_service():
        data = request.json
        logging.info("Received request: CREATE service with data: %s", data)
        # TODO: Add Pydantic validation here for 'data' against your Service DTO schema
        try:
            created = catalog_service.create_service(data)
            return jsonify(format_response(created)), 201
        except Exception as e:
            logging.error("Error creating service: %s", e)
            return jsonify(format_error_response(str(e), "CREATE_ERROR", 500)), 500


    @bp.route('/services/<service_id>', methods=['PUT'])
    def update_service(service_id):
        data = request.json
        logging.info("Received request: UPDATE service %s with data: %s", service_id, data)
        # TODO: Add Pydantic validation here for 'data' against your Service Update DTO schema
        try:
            updated = catalog_service.update_service(service_id, data)
            if not updated:
                return jsonify(format_error_response("Service not found", "NOT_FOUND", 404)), 404
            return jsonify(format_response(updated)), 200
        except Exception as e:
            logging.error("Error updating service: %s", e)
            return jsonify(format_error_response(str(e), "UPDATE_ERROR", 500)), 500

    @bp.route('/services/<service_id>', methods=['DELETE'])
    def delete_service(service_id):
        logging.info("Received request: DELETE service %s", service_id)
        try:
            catalog_service.delete_service(service_id)
            return jsonify({"message": "Service soft-deleted successfully"}), 200
        except Exception as e:
            logging.error("Error deleting service: %s", e)
            return jsonify(format_error_response(str(e), "DELETE_ERROR", 500)), 500

    return bp
