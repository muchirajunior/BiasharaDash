from datetime import datetime
from sqlalchemy import JSON
from main import db

class Business(db.Model):
    __tablename__="businesses"
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(200),nullable=False)
    email=db.Column(db.String(50),unique=True)
    username=db.Column(db.String(50),unique=True,nullable=False)
    address=db.Column(db.String(200))
    cartegory=db.Column(db.String(100))
    phone=db.Column(db.String(20),unique=True)
    photo=db.Column(db.String(200))
    pdf_menu=db.Column(db.String(200))
    website=db.Column(db.String(300))
    subscription=db.Column(db.Float,default=100)
    active=db.Column(db.Boolean,default=True)
    items_cartegories=db.Column(JSON,default=[])
    created_at=db.Column(db.DateTime,default=datetime.now())
    updated_at=db.Column(db.DateTime)
    users=db.relationship("User",backref='businesses',lazy=True)
    items=db.relationship("Item",backref='businesses',lazy=True)
    orders=db.relationship("Order",backref='businesses',lazy=True)

    def __init__(self,name,username,address,cartegory,phone,password):
        self.name=name
        self.username=username
        self.address=address
        self.cartegory=cartegory
        self.phone=phone
        self.password=password