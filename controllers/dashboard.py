from flask import Blueprint, render_template
from flask_login import login_required,current_user
dashboard=Blueprint("dashboard",__name__,url_prefix="/dashboard",template_folder="../templates/dashboard")
   
@dashboard.route("/")
@login_required
def index():
    return render_template("dash_index.html")