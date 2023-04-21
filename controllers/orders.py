from datetime import datetime
from flask import Blueprint, render_template,redirect,request,flash
from flask_login import current_user, login_required
from models.order import Order,db
from models.order_items import OrderItem
from models.item import Item


orders=Blueprint("orders",__name__,url_prefix="/orders",template_folder="../templates/orders")
    
@orders.route("/",methods=['POST','GET'])
@login_required
def orders_route():
    date=datetime.today()
    print(date)
    if request.method == 'POST':
        date=datetime.strptime(request.form.get('date'),"%Y-%m-%d")
    
    start= date.replace(hour=0,minute=0)
    end=date.replace(hour=23,minute=59)
       
    search=request.args.get('search')
    if search==None:
        search=''
    business_orders=Order.query.filter(
        Order.business_id==current_user.business_id,
        Order.sold==False,
        Order.created_at <= end,
        Order.created_at >=start,
        Order.customer.like(f"%{search}%")
        ).order_by(Order.created_at.desc()).all()
    
    return render_template("orders.html",orders=business_orders,date=date)

@orders.route("/add",methods=['POST','GET'])
@login_required
def orders_add_route():
    if request.method == 'POST':
        customer=request.form.get('customer')
        db.session.add(Order(customer,0,current_user.business_id))
        db.session.commit()
    return redirect('/orders')

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
        order.updated_at=datetime.now()
        db.session.commit()
    search=request.args.get('search')
    if search==None:
        search=''

    items=Item.query.filter(Item.business_id==current_user.business_id,Item.active,Item.name.like(f"%{search}%")).all()
    order_items=OrderItem.query.filter_by(order_id=order.id).all()
    return render_template("order_page.html",order=order,order_items=order_items,items=items,search=search)

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
    order.updated_at=datetime.now()
    db.session.delete(item)
    db.session.commit()

    return redirect(request.referrer)

@orders.route("/<id>/complete")
@login_required
def order_complete_route(id):
    order:Order= Order.query.filter(Order.id==id,Order.sold ==False,Order.business_id==current_user.business_id).first()
    if order == None :
        return redirect(request.referrer)
    order_items=OrderItem.query.filter_by(order_id=order.id).all()
    print(order_items)
    if  not order_items or order.total == 0:
        flash('no items for this order')
        return redirect(request.referrer)
    for order_item in order_items:
        item=Item.query.filter_by(id=order_item.item_id).first()
        if item.type == "product":
            if (item.stock < order_item.quantity):
                flash(f"no enough stock for {item.name}")
                return redirect(request.referrer)
            item.stock-=order_item.quantity

    order.sold=True
    order.updated_at=datetime.now()
    db.session.commit()
    return redirect("/orders/sales")

@orders.route("/sales",methods=['POST','GET'])
@login_required
def sales_route():
    date=datetime.today()
    if request.method == 'POST':
        date=datetime.strptime(request.form.get('selldate'),"%Y-%m-%d")
    
    start= date.replace(hour=0,minute=0)
    end=date.replace(hour=23,minute=59)
       
    search=request.args.get('search')
    if search==None:
        search=''
    business_sales=Order.query.filter(
        Order.business_id==current_user.business_id,
        Order.sold==True,
        Order.created_at <= end,
        Order.created_at >=start,
        Order.customer.like(f"%{search}%")
        ).order_by(Order.created_at.desc()).all()
    
    return render_template("sales.html",orders=business_sales,date=date)

@orders.route("/sales/<id>")
@login_required
def sale_route(id):
    order= Order.query.filter(Order.id==id,Order.sold ==True,Order.business_id==current_user.business_id).first()
    if order == None:
        return redirect(request.referrer)

    order_items=OrderItem.query.filter_by(order_id=order.id).all()
    return render_template("sale_page.html",order=order,order_items=order_items)

@orders.route("/sales/<id>/reverse")
@login_required
def sale_reverse_route(id):
    order:Order= Order.query.filter(Order.id==id,Order.sold ==True,Order.business_id==current_user.business_id).first()
    if order == None:
        return redirect(request.referrer)
    order.sold=False
    db.session.commit()
    return redirect("/orders/"+id)