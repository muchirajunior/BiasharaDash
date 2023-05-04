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
    subscription_type=db.Column(db.String(10),default='standard') #basic/standard/premium
    active=db.Column(db.Boolean,default=True)
    items_cartegories=db.Column(JSON,default=[])
    items_count=db.Column(db.Integer)
    today_orders=db.Column(db.Integer) #total orders today
    max_items=db.Column(db.Integer,default=50) #maximumn number of items the business can have
    max_orders=db.Column(db.Integer,default=100) #maximum number of order per day
    created_at=db.Column(db.DateTime,default=datetime.now())
    updated_at=db.Column(db.DateTime)
    users=db.relationship("User",backref='businesses',lazy=True)
    items=db.relationship("Item",backref='businesses',lazy=True)
    orders=db.relationship("Order",backref='businesses',lazy=True)
    customers=db.relationship("Customer",backref='businesses',lazy=True)
    traffic=db.relationship("Traffic",backref='businesses',lazy=True)

    def __init__(self,name,username,address,cartegory,phone):
        self.name=name
        self.username=username
        self.address=address
        self.cartegory=cartegory
        self.phone=phone