from config import app
from controllers.user import users
from controllers.dashboard import dashboard

#register blueprints
app.register_blueprint(users)
app.register_blueprint(dashboard)

if __name__=="__main__":
    app.run(debug=True,port=5000)