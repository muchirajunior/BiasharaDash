from flask import redirect,request
from flask_login import login_required,current_user

def custom_login_required(role):
    def wrapper(fn):
        @login_required
        def decorated_view(*args, **kwargs):
            if not (current_user.role == role or current_user.role == 'admin'):
                return redirect(request.referrer)
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

def upload_file(file):
    print(file)

    return "filename"