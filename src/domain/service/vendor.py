class vendor:
    def __init__(self,id,name,contact,rating):
        self.id=id
        self.name=name
        self.contact = contact
        self.rating=rating
    def __repr__(self):
        return  f"<vendor:{self.name}(Rating: {self.rating})>"