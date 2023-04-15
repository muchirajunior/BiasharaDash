#type: ignore
import argparse
from flask import redirect,request, url_for
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, current_user
from main import app,db,bcrypt
from models.item import Item
from models.user import User
from models.business import Business
from models.order import Order
from models.order_items import OrderItem
from models.cartegory import Cartegory

#declare and initialize login manager for the flask app
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view="users.login" #if user is not login redirect to login route

#create login the decorator
@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

#create admin/super user
def create_super_user():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('--email',required=True)
        parser.add_argument('--password',required=True)
        args = parser.parse_args()
        password=bcrypt.generate_password_hash(args.password,10).decode('utf-8')
        user=User(name="Administrator",email=args.email,password=password)
        user.role="admin"
        db.session.add(user)
        db.session.commit()
        print("(: supper user created successfully :)")
    except Exception as error:
        print(str(error.args))


#create a custom model view for protected and customized settings admin view
class AdminModelView(ModelView):
    can_export=True
    can_view_details=True
    can_set_page_size=True
    column_display_all_relations=False
    form_columns_width='400px'
    form_excluded_columns=['password']
    # create_modal = True
    # edit_modal = True
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role=="admin"
                
    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for("users.restricted"))
        # redirect to login page if user doesn't have access
        return redirect(url_for('users.login', next=request.url))

#setup the flask admin page
admin=Admin(app,template_mode="bootstrap4",)
admin.add_view( AdminModelView(User, db.session)) 
admin.add_view( AdminModelView(Business, db.session)) 
admin.add_view( AdminModelView(Item, db.session))
admin.add_view( AdminModelView(Order, db.session))
admin.add_view( AdminModelView(OrderItem, db.session))
admin.add_view( AdminModelView(Cartegory, db.session))


if __name__=="__main__":
    create_super_user()
