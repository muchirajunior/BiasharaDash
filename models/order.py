from datetime import datetime
from main import db

class Order(db.Model):
    __tablename__='orders'
    id=db.Column(db.Integer,primary_key=True)
    customer=db.Column(db.String(100),nullable=False)
    contact=db.Column(db.String(50))
    address=db.Column(db.String(100))
    delivery_date=db.Column(db.DateTime)
    total=db.Column(db.Float)
    sold=db.Column(db.Boolean,default=False)
    created_at=db.Column(db.DateTime,default=datetime.now())
    updated_at=db.Column(db.DateTime)
    business_id=db.Column(db.Integer,db.ForeignKey("businesses.id"),nullable=False)
    items=db.relationship('OrderItem',backref='orders',lazy=True)

    def __init__(self,customer,contact,address,total,delivery_date,business_id):
        self.customer=customer
        self.contact=contact
        self.address=address
        self.delivery_date=delivery_date
        self.total=total
        self.business_id=business_id

    
