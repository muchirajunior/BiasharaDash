from main import db

class Traffic(db.Model):
    __tablename__='traffic'
    id=db.Column(db.Integer,primary_key=True)