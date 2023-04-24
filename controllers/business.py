from flask import Blueprint, render_template,jsonify,request,redirect
from flask_login import login_required,current_user
from models.business import Business,db
from schemas import businessSchema
from utils  import upload_file

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
        db.session.commit()
    
    return redirect(request.referrer)