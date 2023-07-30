from datetime import datetime
from flask import Blueprint, flash, render_template,request,redirect
from flask_login import login_required,current_user
from models.business import Business
from models.item import Item,db
from utils import upload_file


sales=Blueprint("sales",__name__,url_prefix="/sales",template_folder="../templates/sales")

@sales.route("/<type>", methods=['POST','GET'])
@login_required
def index(type):

    return render_template("documents.html")

@sales.route("/<type>/<id>", methods=['POST','GET'])
@login_required
def index(type,id):

    return render_template("document.html")