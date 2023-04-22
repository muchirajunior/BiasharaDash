from flask import redirect,request
from flask_login import login_required,current_user
from flask_mail import Message
from main import mail
from models.business import Business

def custom_login_required(role):
    def wrapper(fn):
        @login_required
        def decorated_view(*args, **kwargs):
            if not (current_user.role == role or current_user.role == 'admin'):
                return redirect(request.referrer)
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper


#optimize to add it to session
def businessData():
    try:
        business:Business=Business.query.filter_by(id=current_user.business_id).first()
        print(business)
        return business
    except:
        return None

def upload_file(file):
    print(file)

    return "filename"

def sendMail(email,message):
    pass
