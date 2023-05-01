from datetime import datetime
from main import db

class Traffic(db.Model):
    __tablename__='traffic'
    id=db.Column(db.Integer,primary_key=True)
    source=db.Column(db.String(100))
    user=db.Column(db.String(100))
    info=db.Column(db.String(300))
    business=db.Column(db.String(100))
    time=db.Column(db.DateTime,default=datetime.now())
    business_id=db.Column(db.Integer,db.ForeignKey('businesses.id'),nullable=False)

    def __init__(self,source,user,info,business,business_id):
        self.source=source
        self.user=user
        self.info=info
        self.business=business
        self.business_id=business_id
