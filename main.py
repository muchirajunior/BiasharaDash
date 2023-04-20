#type: ignore
from datetime import timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///database.db" #postgresql://username:pass@localhost:5432/database
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config["SECRET_KEY"]="ths973ydj28"
app.config['FLASK_ADMIN_FLUID_LAYOUT'] = True

ma=Marshmallow(app)
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
migrate=Migrate(app,db)


app.permanent_session_lifetime=timedelta(minutes=50) #user session lifetime
