import requests
from flask import redirect,request
from flask_login import login_required,current_user
from models.business import Business
from werkzeug.utils import secure_filename


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
        return business 

    except Exception as error:
        print("fetch business data error ::>"+str(error))
        return None

def upload_file(file):
    try:
        url = 'http://127.0.0.1:8000'# 'https://filesapi.biashara.buzz/'
        filetype="image"
        filename = secure_filename(file.filename)
        ext=filename.rsplit('.',1)[1]
        if ext=='pdf':
            url+='/files'
            filetype='pdf'
        print(filename)
        response = requests.post(url, files={filetype: file})
        print(response.json())
        if response.status_code==200:
            return response.json()['filename']
        else:
            print('failed to upload file')
            return None

    except Exception as error:
        print(str(error))
        return None

def sendMail(email,message):
    pass
