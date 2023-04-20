from config import app
from controllers.user import users
from controllers.dashboard import dashboard,businessData
from controllers.orders import orders
from controllers.business import business

#sets business data to global reach by jinja2 in all files
app.jinja_env.globals.update(businessData=businessData)

#register blueprints
app.register_blueprint(users)
app.register_blueprint(dashboard)
app.register_blueprint(orders)
app.register_blueprint(business)

if __name__=="__main__":
    app.run(debug=True,port=5000)