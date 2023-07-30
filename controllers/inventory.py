from datetime import datetime
from flask import Blueprint, flash, render_template,request,redirect
from flask_login import login_required,current_user
from models.business import Business
from models.item import Item,db
from utils import upload_file


inventory=Blueprint("inventory",__name__,url_prefix="/inventory",template_folder="../templates/inventory")

@inventory.route("/", methods=['POST','GET'])
@login_required
def index():

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
        type=request.form.get("type")
        cartegory=request.form.get("cartegory")
        photo=request.form.get("photo")

        db.session.add(Item(name,price,description,stock,photo,type,cartegory,current_user.business_id))
        business.items_count=count+1
        db.session.commit()
        flash("added item successfully ")
        redirect("/inventory")

    
    cartegories=Business.query.filter_by(id=current_user.business_id).first().items_cartegories
    search=''
    if (request.args.get('search') != None):
        search=request.args.get('search')
    items= Item.query.filter(Item.business_id==current_user.business_id, Item.name.like(f"%{search}%")).order_by(Item.id.asc()).all()

    return render_template("items.html",items=items,cartegories=cartegories,type='')

@inventory.route("/<id>",methods=["POST"])
@login_required
def products_update(id):
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

    return redirect(request.referrer)


@inventory.route('/<id>/delete')
@login_required
def delete_item(id):
    item:Item=Item.query.filter_by(id=id).first()
    print(item)
    if item != None:
        db.session.delete(item)
        db.session.commit()
        flash('deleted item successfully')
    return redirect(request.referrer)

@inventory.route("/cartegories",methods=['POST','GET'])
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