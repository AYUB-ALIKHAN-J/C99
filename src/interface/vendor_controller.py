from flask import Blueprint, request, jsonify
from typing import Optional, Dict, Any, List
from .utils import format_response, format_error_response # Import utility functions

def create_vendor_controller(vendor_service):
    bp = Blueprint('vendor', __name__)

    @bp.route('/vendors', methods=['GET'])
    def list_vendors():
        # Filters from request arguments
        filters = {k: v for k, v in request.args.items()}
        vendors = vendor_service.list_vendors(filters)
        return jsonify(format_response(vendors)), 200

    @bp.route('/vendors/<vendor_id>', methods=['GET'])
    def vendor_details(vendor_id):
        vendor = vendor_service.get_vendor_details(vendor_id)
        if not vendor:
            return jsonify(format_error_response("Vendor not found", "NOT_FOUND", 404)), 404
        return jsonify(format_response(vendor)), 200

    @bp.route('/vendors', methods=['POST'])
    def create_vendor():
        data = request.json
        # TODO: Add Pydantic validation here for 'data' against your Vendor DTO schema
        try:
            created = vendor_service.create_vendor(data)
            return jsonify(format_response(created)), 201
        except Exception as e:
            return jsonify(format_error_response(str(e), "CREATE_ERROR", 500)), 500

    @bp.route('/vendors/<vendor_id>', methods=['PUT'])
    def update_vendor(vendor_id):
        data = request.json
        # TODO: Add Pydantic validation here for 'data' against your Vendor Update DTO schema
        try:
            updated = vendor_service.update_vendor(vendor_id, data)
            if not updated:
                return jsonify(format_error_response("Vendor not found", "NOT_FOUND", 404)), 404
            return jsonify(format_response(updated)), 200
        except Exception as e:
            return jsonify(format_error_response(str(e), "UPDATE_ERROR", 500)), 500

    @bp.route('/vendors/<vendor_id>', methods=['DELETE'])
    def delete_vendor(vendor_id):
        try:
            vendor_service.delete_vendor(vendor_id)
            return jsonify({"message": "Vendor soft-deleted successfully"}), 200
        except Exception as e:
            return jsonify(format_error_response(str(e), "DELETE_ERROR", 500)), 500

    return bp
