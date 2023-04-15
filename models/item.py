from datetime import datetime
from main import db

class Item(db.Model):
    __tablename__='items'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50),nullable=False)
    price=db.Column(db.Float,nullable=False)
    description=db.Column(db.String)
    stock=db.Column(db.Integer)
    type=db.Column(db.String(10),default="product")#product/service
    active=db.Column(db.Boolean,default=True)
    photo=db.Column(db.String)
    photo_2=db.Column(db.String)
    photo_3=db.Column(db.String)
    created_at=db.Column(db.DateTime,default=datetime.now())
    updated_at=db.Column(db.DateTime)
    business_id=db.Column(db.Integer,db.ForeignKey('businesses.id'),nullable=False)
    

    def __init__(self,name,price,description,photo,type,business_id):
        self.name=name
        self.price=price
        self.description=description
        self.photo=photo
        self.type=type
        self.business_id=business_id