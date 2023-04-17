import json
from flask import Blueprint, render_template,request,redirect
from flask_login import login_required,current_user
from models.business import Business
from models.item import Item,db

dashboard=Blueprint("dashboard",__name__,url_prefix="",template_folder="../templates/dashboard")
   
@dashboard.route("/")
@login_required
def index():
    cartegories=Business.query.filter_by(id=current_user.business_id).first().items_cartegories
    return render_template("dash_index.html",cartegories=cartegories)


@dashboard.route("/dashboard/")
@login_required
def index_route():
    cartegories=Business.query.filter_by(id=current_user.business_id).first().items_cartegories
    return render_template("dash_index.html",cartegories=cartegories)

@dashboard.route("/<type>",methods=["POST","GET"])
@login_required
def itemss_route(type):
    if request.method=="POST":
        name=request.form.get("name")
        price=request.form.get("price")
        stock=request.form.get("stock")
        description=request.form.get("description")
        cartegory=request.form.get("cartegory")
        photo=request.form.get("photo")

        db.session.add(Item(name,price,description,stock,photo,type,cartegory,current_user.business_id))
        db.session.commit()

    items= Item.query.filter(Item.business_id==current_user.business_id, Item.type==type).all()
    cartegories=Business.query.filter_by(id=current_user.business_id).first().items_cartegories

    return render_template("items.html",items=items,cartegories=cartegories)

@dashboard.route("/<type>/<id>",methods=["POST"])
@login_required
def products_update(type,id):
    if request.method=="POST":
        item:Item=Item.query.filter_by(id=id).first()
        item.name=request.form.get("name")
        item.price=request.form.get("price")
        item.stock=request.form.get("stock")
        item.description=request.form.get("description")
        item.cartegory=request.form.get("cartegory")
        active=request.form.get("active")
        if active=='on':
            item.active=True
        else:
            item.active=False
        item.photo=request.form.get("photo")
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


@dashboard.route("orders",methods=["POST","GET"])
@login_required
def orders_route():

    return render_template('orders.html')