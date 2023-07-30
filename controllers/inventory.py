from datetime import datetime
from flask import Blueprint, flash, render_template,request,redirect
from flask_login import login_required,current_user
from models.business import Business
from models.item import Item,db
from models.customer import Customer
from models.cartegory import Cartegory
from utils import custom_login_required,upload_file


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
        cartegory=request.form.get("cartegory")
        photo=request.form.get("photo")

        db.session.add(Item(name,price,description,stock,photo,type,cartegory,current_user.business_id))
        business.items_count=count+1
        db.session.commit()

        return  redirect(f"/{type}")

    
    cartegories=Business.query.filter_by(id=current_user.business_id).first().items_cartegories
    search=''
    if (request.args.get('search') != None):
        search=request.args.get('search')
    items= Item.query.filter(Item.business_id==current_user.business_id, Item.name.like(f"%{search}%")).order_by(Item.id.asc()).all()

    return render_template("items.html",items=items,cartegories=cartegories,type='')

    render_template("items.html")