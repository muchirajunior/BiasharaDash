from datetime import datetime
from flask import Blueprint, flash, render_template,request,redirect
from flask_login import login_required,current_user
from models.business import Business
from models.item import Item,db
from models.customer import Customer
from models.cartegory import Cartegory
from utils import custom_login_required,upload_file


dashboard=Blueprint("dashboard",__name__,url_prefix="",template_folder="../templates/dashboard")

@dashboard.route("/")
@login_required
def index():
    # print(request.headers)
    print(f"{current_user.business_id},{str(datetime.now()).split('.')[0]},{current_user.name},{request.remote_addr}")
  
    return render_template("business_dash.html")


@dashboard.route("/dashboard/")
@login_required
def index_route():
    business_cartegories=Cartegory.query.all()
    return render_template("business_dash.html",business_cartegories=business_cartegories)

@dashboard.route("/<type>",methods=["POST","GET"])
@login_required
def items_route(type):
    if not (type == 'product' or type == 'service'):  
        return redirect('/')

    if request.method=="POST":
        business:Business=Business.query.get(current_user.business_id)
        count=Item.query.filter(Item.business_id==current_user.business_id).count()
        if count >= business.max_items:
            flash('you have reached the maximum Items you can upload. upgrade for to increase your limit!')
            return redirect(request.referrer)
        name=request.form.get("name")
        price=request.form.get("price")
        stock=request.form.get("stock")
        description=request.form.get("description")
        cartegory=request.form.get("cartegory")
        photo=request.form.get("photo")

        db.session.add(Item(name,price,description,stock,photo,type,cartegory,current_user.business_id))
        business.items_count=count+1
        db.session.commit()

        return  redirect(f"/{type}")

    
    cartegories=Business.query.filter_by(id=current_user.business_id).first().items_cartegories
    if (request.args.get('search') != None):
        search=request.args.get('search')
        items= Item.query.filter(Item.business_id==current_user.business_id, Item.type==type,Item.name.like(f"%{search}%")).all()
    else:
        items= Item.query.filter(Item.business_id==current_user.business_id, Item.type==type).all()
       
    return render_template("items.html",items=items,cartegories=cartegories,type=type)

@dashboard.route("/<type>/<id>",methods=["POST"])
@login_required
def products_update(type,id):
    if request.method=="POST":
        item:Item=Item.query.filter_by(id=id).first()
        item.name=request.form.get("name")
        item.price=request.form.get("price")
        if request.form.get("stock") != '' :
            item.stock=request.form.get("stock")
        item.description=request.form.get("description")
        if(request.form.get("cartegory") != None):
            item.cartegory=request.form.get("cartegory")
        if(request.form.get("vat") != None):
            item.vat=request.form.get("vat")
        active=request.form.get("active")
        if active=='on':
            item.active=True
        else:
            item.active=False
        if(request.files["photo"] != None):
            print(request.files["photo"])
            filename= upload_file(request.files["photo"])
            print(request.files["photo"])
            if filename != None:
                item.photo=filename
        item.updated_at=datetime.now()
        db.session.commit()

    return redirect("/"+type)

@dashboard.route('delete/<type>/<id>')
@login_required
def delete_item(type,id):
    item:Item=Item.query.filter_by(id=id).first()
    print(item)
    if item != None:
        db.session.delete(item)
        db.session.commit()
    
    return redirect('/'+type)

@dashboard.route("/cartegories",methods=['POST','GET'])
@login_required
def item_cartegories_route():
    if request.method == 'POST':
        item=request.form.get('cartegory')
        business:Business=Business.query.filter_by(id=current_user.business_id).first()
        if business.items_cartegories== None or isinstance(business.items_cartegories,dict) :
            business.items_cartegories=[item]
        elif isinstance(business.items_cartegories,list):
            business.items_cartegories=business.items_cartegories+[item] #concatinate arrays to add up
        db.session.commit()
    return  redirect(request.referrer)



@dashboard.route("/customers",methods=['POST','GET'])
@login_required
def customers_route():
    if request.method =="POST":
        name=request.form.get('name')
        phone=request.form.get('phone')
        email=request.form.get('email')
        address=request.form.get('address')
        db.session.add(Customer(name,address,phone,email,current_user.business_id))
        db.session.commit()

        return redirect('/customers')
    search=''
    if (request.args.get('search') != None):
        search=request.args.get('search')
    customers = Customer.query.filter(Customer.business_id==current_user.business_id,Customer.name.like(f"%{search}%")).all()
    return render_template('customers.html',customers=customers)

@dashboard.route("/customers/<id>",methods=['POST','GET'])
@login_required
def customer_route(id):
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

@dashboard.route("/customers/<id>/delete")
@login_required
def customer_delete_route(id):
    customer = Customer.query.filter_by(id=id,business_id=current_user.business_id).first()
    if customer == None:
        return redirect(request.referrer)
    db.session.delete(customer)
    db.session.commit()

    return redirect(request.referrer)
