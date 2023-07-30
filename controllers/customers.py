from flask import Blueprint, render_template,redirect,request,flash
from flask_login import current_user, login_required
from models.order import db
from models.business import Business
from models.customer import Customer


customers=Blueprint("customers",__name__,url_prefix="/customers",template_folder="../templates/customers")
    
@customers.route("/",methods=['POST','GET'])
@login_required
def index():
    if request.method =="POST":
        business:Business=Business.query.get(current_user.business_id)
        count=Customer.query.filter_by(business_id=current_user.business_id).count()
        if count >= business.max_customers:
            flash('you have reached the maximum customers you can upload. upgrade for to increase your limit!')
            return redirect(request.referrer)
        name=request.form.get('name')
        phone=request.form.get('phone')
        email=request.form.get('email')
        address=request.form.get('address')
        db.session.add(Customer(name,address,phone,email,current_user.business_id))
        business.customers_count=count+1
        db.session.commit()

        return redirect('/customers')
    search=''
    if (request.args.get('search') != None):
        search=request.args.get('search')
    customers = Customer.query.filter(Customer.business_id==current_user.business_id,Customer.name.like(f"%{search}%")
                ).order_by(Customer.id.asc()).all()
    return render_template('customers.html',customers=customers)

@customers.route("/<id>",methods=['POST','GET'])
@login_required
def customer_update_route(id):
    customer = Customer.query.filter_by(id=id,business_id=current_user.business_id).first()
    if customer == None:
        return redirect(request.referrer)
    if request.method =="POST":
        customer.name=request.form.get('name')
        customer.phone=request.form.get('phone')
        customer.email=request.form.get('email')
        customer.address=request.form.get('address')
        db.session.commit()

    return redirect(request.referrer) 

@customers.route("/<id>/delete")
@login_required
def customer_delete_route(id):
    customer = Customer.query.filter_by(id=id,business_id=current_user.business_id).first()
    if customer == None:
        return redirect(request.referrer)
    db.session.delete(customer)
    db.session.commit()

    return redirect(request.referrer)


