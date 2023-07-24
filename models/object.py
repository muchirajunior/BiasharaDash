from main import db

class Object(db.Model):
    __tablename__='objects'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20),nullable=False)
    number=db.Column(db.Integer,nullable=False)

    def __init__(self,name,number):
        self.name=name
        self.number=number