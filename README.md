# C99 Catalog Microservice

## Overview

This microservice manages the catalog of services and vendors for a marketplace platform.  
It provides RESTful APIs for CRUD operations, filtering, and searching of services and vendors.

---

## Features

- **Service Management:** Create, update, list, delete, and search services.
- **Vendor Management:** Create, update, list, and delete vendors.
- **Filtering & Pagination:** List endpoints support filtering, sorting, and pagination.
- **Soft Delete:** Services and vendors are soft-deleted (not removed from DB).
- **System Fields:** Fields like `id`, `created_at`, `updated_at`, `status`, and `is_deleted` are managed by the backend.
- **Logging:** All key actions and errors are logged to the terminal for developer visibility.
- **Environment Config:** MongoDB connection details are managed via a `.env` file.

---

## Project Structure

```
project/
├── main.py
├── .env
├── requirements.txt
├── README.md
├── src/
│   ├── domain/
│   │   └── service/
│   │       ├── service.py
│   │       ├── vendor.py
│   │       └── value_objects.py
│   ├── infrastructure/
│   │   ├── service_repository.py
│   │   └── vendor_repository.py
│   ├── application/
│   │   ├── catalog_service.py
│   │   └── vendor_service.py
│   └── interface/
│       ├── catalog_controller.py
│       ├── vendor_controller.py
│       ├── search_controller.py
│       └── utils.py
└── tests/
    └── test_catalog.py
```

---

## Environment Setup

1. **Clone the repository**
2. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```
3. **Configure environment variables**  
   Create a `.env` file in the project root:
   ```
   MONGO_URL=mongodb://localhost:27017/
   MONGO_DB_NAME=service_catalog
   ```
4. **Start MongoDB** (ensure it is running on the configured host/port)

---

## Running the Service

```sh
python main.py
```

The service will be available at `http://localhost:5000/`.

---

## API Endpoints

### Service Endpoints

- `GET /services` — List services (supports filtering, pagination, sorting)
- `GET /services/<service_id>` — Get service details
- `POST /services` — Create a new service
- `PUT /services/<service_id>` — Update a service
- `DELETE /services/<service_id>` — Soft-delete a service
- `GET /services/search?q=...` — Search services

### Vendor Endpoints

- `GET /vendors` — List vendors
- `GET /vendors/<vendor_id>` — Get vendor details
- `POST /vendors` — Create a new vendor
- `PUT /vendors/<vendor_id>` — Update a vendor
- `DELETE /vendors/<vendor_id>` — Soft-delete a vendor

---

## Testing

Run all tests with:

```sh
pytest
```

See `tests/test_catalog.py` for example test cases covering all endpoints.

---

## Logging

All major actions and errors are logged to the terminal for easy debugging and monitoring.

---

## Notes

- System-managed fields (`id`, `created_at`, `updated_at`, `status`, `is_deleted`) are handled by the backend.
- Only user-input fields need to be provided in API requests.
- The microservice is ready for integration with cart and booking services.

---

## Example cURL Commands

```sh
# Create a service
curl -X POST http://localhost:5000/services \
  -H "Content-Type: application/json" \
  -d '{"name": {"en": "Test Hall"}, "description": {"en": "A test hall"}, "category": "venue", "vendor_id": "vendor1"}'

# List services
curl -X GET http://localhost:5000/services

# Create a vendor
curl -X POST http://localhost:5000/vendors \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Vendor", "contact": {"email": "test@vendor.com"}, "rating": {"average": 5.0, "count": 1}}'
```

---

## License

MIT License