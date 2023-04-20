from flask import Blueprint, render_template,jsonify
from flask_login import login_required,current_user
from models.business import Business
from schemas import businessSchema

business=Blueprint("businesses",__name__,url_prefix="/business",template_folder="../templates/business")

@business.route("/")
@login_required
def index():
    return render_template("business.html")

@business.route('/<username>')
def business_api(username:str):
    business:Business = Business.query.filter_by(username=username).first()
    if business == None :
        return jsonify(error='not found',message='business with such username not found'),404
    elif business.active == False:
        return jsonify(error='inactive business',message='the named business is inactive or out of service'),400
    
    bs=businessSchema.dump(business)

    return jsonify(bs)
    