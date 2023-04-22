from datetime import datetime
from main import db

class Customer(db.Model):
    __tablename__='customers'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),nullable=False)
    address=db.Column(db.String(50))
    phone=db.Column(db.String(14))
    email=db.Column(db.String(30))
    created_at=db.Column(db.DateTime,default=datetime.now())
    updated_at=db.Column(db.DateTime)
    business_id=db.Column(db.Integer,db.ForeignKey('businesses.id'),nullable=False)
    
    def __init__(self,name,address,phone,email,business_id):
        self.name=name
        self.address=address
        self.phone=phone
        self.email=email
        self.business_id=business_id