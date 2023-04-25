from flask import redirect,request,session
from flask_login import login_required,current_user
from models.business import Business
from werkzeug.utils import secure_filename
from shortuuid import uuid
from PIL import Image
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
        # current_time=datetime.now()
        # last_query=session['last_query']

        # if session.get('business')== None:
        #     print("no session")
        #     business:Business=Business.query.filter_by(id=current_user.business_id).first()
        #     bs=business.__dict__
        #     bs.pop('_sa_instance_state')
        #     session['business']=bs
        # return session['business'] 
        return Business.query.filter_by(id=current_user.business_id).first()

    except Exception as error:
        print("fetch business data error ::>"+str(error))
        return None

def upload_file(file):
    try:
        path = '/home/muchirajunoir/Downloads/filesapi'
        filename = secure_filename(file.filename)
        ext=filename.rsplit('.',1)[1]
        filename=uuid()+'.'+ext
        if ext=='pdf':
            file.save(f"{path}/pdfs/{filename}")
        else:
            image=Image.open(file)
            image=image.resize((320,240))
            image.save(f"{path}/images/{filename}")
        
        return filename

    except Exception as error:
        print(str(error))
        return None

def sendMail(email,message):
    pass
