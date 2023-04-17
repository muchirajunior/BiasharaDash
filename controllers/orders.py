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
    business_orders=Order.query.order_by(Order.created_at.desc()).filter_by(business_id=current_user.business_id,sold=False).all()
    return render_template("orders.html",orders=business_orders)

@orders.route("/<id>",methods=['POST','GET'])
@login_required
def order_route(id):
    order= Order.query.filter(Order.id==id,Order.sold ==False,Order.business_id==current_user.business_id).first()
    if order == None:
        return redirect('/orders')
    
    if request.method == 'POST':
        name=request.form.get('name')
        quantity=request.form.get('quantity')
        price=request.form.get('price')
        item_id=request.form.get('item_id')
        db.session.add(OrderItem(name,price,quantity,item_id,order.id))
        order.total+=float(price)*int(quantity)
        db.session.commit()
    search=request.args.get('search')
    if search==None:
        search=''

    items=Item.query.filter(Item.business_id==current_user.business_id,Item.active,Item.name.like(f"%{search}%")).all()
    order_items=OrderItem.query.filter_by(order_id=order.id).all()
    return render_template("order_page.html",order=order,order_items=order_items,items=items)

@orders.route("/<id>/<itemid>")
@login_required
def remove_item_route(id,itemid):
    order:Order= Order.query.filter(Order.id==id,Order.sold ==False,Order.business_id==current_user.business_id).first()
    if order == None:
        return redirect('/orders')
    item:OrderItem=OrderItem.query.filter_by(id=itemid).first()
    if item ==None:
        return redirect('/orders')
    order.total-=item.price*item.quantity
    db.session.delete(item)
    db.session.commit()

    return redirect(request.referrer)