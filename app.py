from config import app
from controllers.user import users
from controllers.dashboard import dashboard
from controllers.orders import orders
from controllers.business import business
from controllers.inventory import inventory
from controllers.customers import customers

#register blueprints
app.register_blueprint(users)
app.register_blueprint(dashboard)
app.register_blueprint(orders)
app.register_blueprint(business)
app.register_blueprint(inventory)
app.register_blueprint(customers)

if __name__=="__main__":
    app.run(debug=True,port=5000)