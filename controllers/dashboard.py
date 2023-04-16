from flask import Blueprint, render_template,request,redirect
from flask_login import login_required,current_user
from models.item import Item,db

dashboard=Blueprint("dashboard",__name__,url_prefix="",template_folder="../templates/dashboard")
   
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
def itemss_route(type):
    if request.method=="POST":
        name=request.form.get("name")
        price=request.form.get("price")
        stock=request.form.get("stock")
        description=request.form.get("description")
        photo=request.form.get("photo")

        db.session.add(Item(name,price,description,stock,photo,type,current_user.business_id))
        db.session.commit()

    items= Item.query.filter(Item.business_id==current_user.business_id, Item.type==type).all()

    return render_template("items.html",items=items)

@dashboard.route("/<type>/<id>",methods=["POST"])
@login_required
def products_update(type,id):
    if request.method=="POST":
        item:Item=Item.query.filter_by(id=id).first()
        item.name=request.form.get("name")
        item.price=request.form.get("price")
        item.stock=request.form.get("stock")
        item.description=request.form.get("description")
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


@dashboard.route("orders",methods=["POST","GET"])
@login_required
def orders_route():

    return render_template('orders.html')