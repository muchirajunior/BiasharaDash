from main import db

class ObjectType(db.Model):
    __tablename__='objecttypes'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20),nullable=False)
    number=db.Column(db.Integer,nullable=False,unique=True)

    def __init__(self,name,number):
        self.name=name
        self.number=number