from main import db

class Message(db.Model):
    __tablename__="messages"
    id=db.Column(db.Integer,primary_key=True)
    sender=db.Column(db.String(30))
    sender_id=db.Column(db.Integer)
    reciever_id=db.Column(db.Integer)
    message=db.Column(db.String(500),nullable=False)
    cartegory=db.Column(db.String(30))
    read=db.Column(db.Boolean,default=False)
    

    def __init__(self,sender,sender_id,receiver_id,message,carteory):
        self.sender=sender
        self.sender_id=sender_id
        self.reciever_id=receiver_id
        self.message=message
        self.cartegory=carteory