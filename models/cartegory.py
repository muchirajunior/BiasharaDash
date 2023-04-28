from main import db

#business cartegories
class Cartegory(db.Model):
    __tablename__="cartegories"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),nullable=False)
    address_name=db.Column(db.String(50))

    def __init__(self,name):
        self.name=name