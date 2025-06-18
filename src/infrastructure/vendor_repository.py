from pymongo import MongoClient

class VendorRepository:
    def __init__(self, mongo_url="mongodb://localhost:27017/", db_name="service_catalog"):
        self.client = MongoClient(mongo_url)
        self.db = self.client[db_name]

    def get_all_vendors(self):
        return list(self.db.vendors.find({}))

    def get_vendor_by_id(self, vendor_id):
        return self.db.vendors.find_one({"id": vendor_id})
