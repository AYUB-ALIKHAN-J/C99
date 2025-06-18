class service:
    def __init__(self, id, name, description, category, price, vendor_id):
        self.id = id
        self.name=name
        self.description = description
        self.category = category
        self.price = price
        self.vendor_id = vendor_id
    
    def __repr__(self):
        return f"<service:{self.name } (Category: {self.category})>"
        