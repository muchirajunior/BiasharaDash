from datetime import timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_mail import Mail
from flask_cors import CORS

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']="postgresql://junior:1234@localhost:5432/biashara"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config["SECRET_KEY"]="ths973ydj28"
app.config['FLASK_ADMIN_FLUID_LAYOUT'] = True
app.config['MAIL_SERVER'] = 'lim106.truehost.cloud'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'non-reply@biashara.buzz'
app.config['MAIL_PASSWORD'] = '@biashara'

ma=Marshmallow(app)
mail=Mail(app)
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
migrate=Migrate(app,db)

CORS(app)
app.permanent_session_lifetime=timedelta(minutes=50) #user session lifetime
