from datetime import datetime
from flask import Blueprint, render_template,request,redirect
from flask_login import login_required,current_user
from models.business import Business
from models.item import Item,db
from models.customer import Customer


dashboard=Blueprint("dashboard",__name__,url_prefix="",template_folder="../templates/dashboard")

def businessData():
    try:
        business:Business=Business.query.filter_by(id=current_user.business_id).first()
        return business
    except:
        return None

@dashboard.route("/")
@login_required
def index():

    return render_template("dash_index.html")


@dashboard.route("/dashboard/")
@login_required
def index_route():

    return render_template("dash_index.html")

@dashboard.route("/<type>",methods=["POST","GET"])
@login_required
def items_route(type):

    if request.method=="POST":
        name=request.form.get("name")
        price=request.form.get("price")
        stock=request.form.get("stock")
        description=request.form.get("description")
        cartegory=request.form.get("cartegory")
        photo=request.form.get("photo")

        db.session.add(Item(name,price,description,stock,photo,type,cartegory,current_user.business_id))
        db.session.commit()

    
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
        item.stock=request.form.get("stock")
        item.description=request.form.get("description")
        if(request.form.get("cartegory") != None):
            item.cartegory=request.form.get("cartegory")
        active=request.form.get("active")
        if active=='on':
            item.active=True
        else:
            item.active=False
        if(request.form.get("photo") != None):
            item.photo=request.form.get("photo")
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
            business.items_cartegories=business.items_cartegories+[item] #conactinate arrays to add up
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
