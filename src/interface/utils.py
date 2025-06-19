from bson.objectid import ObjectId
from typing import Any, Dict, List, Union,Optional

def convert_objectid(data: Union[Dict, List, Any]) -> Union[Dict, List, Any]:
    """
    Recursively converts ObjectId fields within a dictionary or list of dictionaries
    to their string representation for JSON serialization.
    Handles lists of dictionaries and nested dictionaries.
    """
    if isinstance(data, list):
        return [convert_objectid(item) for item in data]
    elif isinstance(data, dict):
        return {
            k: str(v) if isinstance(v, ObjectId) else convert_objectid(v)
            for k, v in data.items()
        }
    else:
        return data

def format_response(data: Any, pagination: Optional[Dict[str, Any]] = None) -> Dict:
    """
    Standardizes the API response format.
    Ensures ObjectIds are converted to strings.
    """
    formatted_data = convert_objectid(data)
    response = {"data": formatted_data}
    if pagination:
        response["pagination"] = pagination
    return response

def format_error_response(message: str, code: str, status_code: int) -> tuple[Dict, int]:
    """
    Standardizes the API error response format.
    """
    return {"error": message, "code": code}, status_code
