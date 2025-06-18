class CatalogService:
    def __init__(self , service_repo,vendor_repo):
        self.service_repo =service_repo
        self.vendor_repo=vendor_repo
    
    def list_services(self):
        return self.service_repo.get_all_services()

    def get_service(self, service_id):
        service = self.service_repo.get_service_by_id(service_id)
        if not service:
            return None
        vendor = self.vendor_repo.get_vendor_by_id(service["vendor_id"])
        service["vendorDetails"] = vendor
        return service
    
    def filter_service(self,filters):
        return self.service_repo.filter_service(filters)
    
    def get_service_details(self, service_id):
        return self.get_service(service_id)