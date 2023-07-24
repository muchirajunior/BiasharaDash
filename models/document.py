from datetime import datetime
from main import db

class Document(db.Model):
    __tablename__='documents'
    id=db.Column(db.Integer,primary_key=True)
    customer=db.Column(db.String(200),nullable=False)
    creator=db.Column(db.String(200),nullable=False)
    contact=db.Column(db.String(50))
    address=db.Column(db.String(100))
    total=db.Column(db.Float)
    vat=db.Column(db.Float,default=0)
    discount=db.Column(db.Float)
    closed=db.Column(db.Boolean,default=False)
    object_type=db.Column(db.Integer,nullable=False)
    base_document=db.Column(db.Integer)
    payment_type=db.Column(db.String(50))
    mpesa_code=db.Column(db.String(20))
    comment=db.Column(db.String(200))
    delivery_date=db.Column(db.DateTime)
    created_at=db.Column(db.DateTime,default=datetime.now())
    updated_at=db.Column(db.DateTime)
    business_id=db.Column(db.Integer,db.ForeignKey("businesses.id"),nullable=False)
    items=db.relationship('DocumentItem',backref='documents',lazy=True)
    customer_id=db.Column(db.Integer,db.ForeignKey("customers.id"),nullable=True)
    creator_id=db.Column(db.Integer,db.ForeignKey("businesses.id"),nullable=False)

    def __init__(self,customer,creator,contact,address,object_type,business_id,creator_id):
        self.customer=customer
        self.creator=creator
        self.contact=contact
        self.address=address
        self.object_type=object_type
        self.business_id=business_id
        self.creator_id=creator_id
