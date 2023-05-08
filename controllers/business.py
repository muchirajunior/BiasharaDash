from flask import Blueprint, flash, render_template,jsonify,request,redirect
from flask_login import login_required,current_user
from models.business import Business,db
from models.cartegory import Cartegory
from models.traffic import Traffic
from schemas import businessSchema,cartegorySchema
from utils  import upload_file
from datetime import datetime

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
    db.session.add(Traffic(source=request.remote_addr, user='customer',info="customer search",business=business.name,business_id=business.id ))
    db.session.commit()
    bs=businessSchema.dump(business)
    print(f"{str(datetime.now()).split('.')[0]},customer,{request.remote_addr},{request.remote_user}")
    cart=None
    if business.cartegory != None:
        cartegory=Cartegory.query.filter_by(name=business.cartegory).first()
        cart=cartegorySchema.dump(cartegory)

    return jsonify(business=bs,cartegory=cart)

@business.route("/profile",methods=['POST','GET'])
@login_required
def profile():
    business:Business = Business.query.get(current_user.business_id)
    if(business== None):
        print("business here",business)
        return redirect(request.referrer)
    if request.method == 'POST':
        business.name=request.form.get('name')
        business.email=request.form.get('email')
        business.address=request.form.get('address')
        business.website=request.form.get('website')
        business.phone=request.form.get('phone')
        business.about=request.form.get('about')
        business.notification=request.form.get('notification')
        if not(request.form.get('cartegory') == None or request.form.get('cartegory') ==''):
            business.cartegory=request.form.get('cartegory')
        if (request.files['pdf_menu'] != None):
            filename= upload_file(request.files['pdf_menu'])
            if filename != None:
                business.pdf_menu=filename
        if (request.files['photo'] != None):
            filename= upload_file(request.files['photo'])
            if filename != None:
                business.photo=filename
        business.updated_at=datetime.now()
        db.session.commit()
    
    return redirect(request.referrer)

@business.route("/export-data",methods=['POST','GET'])
@login_required
def export_data():
    flash("process under maitenance !!")

    return redirect(request.referrer)