from pymongo import MongoClient

class ServiceRepositary:
    def __init__(self,mongo_url="mongodb://localhost:27017/",db_name ="service_catalog"):
        self.client =MongoClient(mongo_url)
        self.db =self.client[db_name]

    def get_all_services(self):
        return list(self.db.services.find({}))
    
    def get_service_by_id(self, service_id):
        return self.db.services.find_one({"id": service_id})
    
    def filter_service(self,filters):
        query ={}
        if "category" in filters:
            query["category"] = filters["category"]
        if "minPrice" in filters and "maxPrice" in filters:
            query["price"] = {"$gte":filters["minPrice"],"$lte":filters["maxPrice"]}
        return list(self.db.services.find(query))