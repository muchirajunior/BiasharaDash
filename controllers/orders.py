from flask import Blueprint, render_template,redirect,request
from flask_login import current_user, login_required
from models.order import Order,db
from models.order_items import OrderItem
from models.item import Item


orders=Blueprint("orders",__name__,url_prefix="/orders",template_folder="../templates/orders")
    
@orders.route("/",methods=['POST','GET'])
@login_required
def orders_route():
    if request.method == 'POST':
        customer=request.form.get('customer')
        db.session.add(Order(customer,0,current_user.business_id))
        db.session.commit()
    business_orders=Order.query.order_by(Order.created_at.desc()).filter_by(business_id=current_user.business_id).all()
    return render_template("orders.html",orders=business_orders)

@orders.route("/<id>",methods=['POST','GET'])
@login_required
def order_route(id):
    order= Order.query.filter(Order.id==id,Order.business_id==current_user.business_id).first()
    if order == None:
        return redirect('/orders')
    search=request.args.get('search')
    if search==None:
        search=''
    items=Item.query.filter(Item.business_id==current_user.business_id,Item.stock>0,Item.name.like(f"%{search}%"))
    order_items=OrderItem.query.filter_by(order_id=order_route.id).all()
    return render_template("order_page.html",order=order,order_items=order_items,items=items)