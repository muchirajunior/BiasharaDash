from main import db

class OrderItem(db.Model):
    __tablename__='ordersitems'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),nullable=False)
    price=db.Column(db.Float,nullable=False)
    quantity=db.Column(db.Integer)
    vat=db.Column(db.Float,default=0)
    discount=db.Column(db.Float,default=0)
    item_id=db.Column(db.Integer)
    order_id=db.Column(db.Integer,db.ForeignKey("orders.id"),nullable=False)

    def __init__(self,name,price,quantity,item_id,vat,order_id):
        self.name=name
        self.price=price
        self.quantity=quantity
        self.item_id=item_id
        self.vat=vat
        self.order_id=order_id

