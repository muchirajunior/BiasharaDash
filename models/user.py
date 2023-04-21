from datetime import datetime
from flask_login import UserMixin
from main import db

class User(db.Model,UserMixin):
    __tablename__="users"
    id:int=db.Column(db.Integer,primary_key=True)
    name:str=db.Column(db.String(50))
    email:str=db.Column(db.String(20),unique=True,nullable=False)
    password:str=db.Column(db.String(200),nullable=False)
    role:str=db.Column(db.String(20),default="user") #user/admin/manager
    active=db.Column(db.Boolean,default=True)
    otp:int=db.Column(db.Integer)
    created_at=db.Column(db.DateTime,default=datetime.now())
    updated_at=db.Column(db.DateTime)
    business_id=db.Column(db.Integer,db.ForeignKey('businesses.id'))
    
    

    def __init__(self,name,email,password):
        self.name=name
        self.email=email
        self.password=password