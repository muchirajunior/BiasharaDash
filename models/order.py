from datetime import datetime
from main import db

class Order(db.Model):
    __tablename__='orders'
    id=db.Column(db.Integer,primary_key=True)
    customer=db.Column(db.String(100),nullable=False)
    total=db.Column(db.Float)
    sold=db.Column(db.Boolean,default=False)
    created_at=db.Column(db.DateTime,default=datetime.now())
    updated_at=db.Column(db.DateTime)
    business_id=db.Column(db.Integer,db.ForeignKey("businesses.id"),nullable=False)
    items=db.relationship('OrderItem',backref='orders',lazy=True)

    def __init__(self,customer,total,business_id):
        self.customer=customer
        self.total=total
        self.business_id=business_id

    
