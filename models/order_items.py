from main import db

class OrderItem(db.Model):
    __tablename__='ordersitems'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),nullable=False)
    price=db.Column(db.Float,nullable=False)
    quantity=db.Column(db.Integer)
    item_id=db.Column(db.Integer)
    order_id=db.Column(db.Integer,db.ForeignKey("orders.id"),nullable=False)

    def __init__(self,name,price,quantity,item_id,order_id):
        self.name=name
        self.price=price
        self.quantity=quantity
        self.item_id=item_id
        self.order_id=order_id

