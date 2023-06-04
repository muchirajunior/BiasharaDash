from datetime import datetime
from flask import Blueprint, jsonify, render_template,redirect,request,flash
from flask_login import current_user, login_required
from models.order import Order,db
from models.order_items import OrderItem
from models.item import Item
from models.business import Business


orders=Blueprint("orders",__name__,url_prefix="/orders",template_folder="../templates/orders")
    
@orders.route("/",methods=['POST','GET'])
@login_required
def orders_route():
    date=datetime.today()
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
        ).order_by(Order.id.desc()).all()
    
    return render_template("orders.html",orders=business_orders,date=date.date())

@orders.route("/create",methods=['POST'])
def post_order_api():
    try:
        business_id=request.json.get('business_id')
        customer=request.json.get('customer')
        contact=request.json.get('contact')
        address=request.json.get('address')
        delivery_date=request.json.get('delivery_date')
        items=request.json.get('items')
        if delivery_date == '':
            delivery_date=None
        if (items != None):
            order:Order = Order(customer,contact,address,0,delivery_date,business_id)
            db.session.add(order)
            db.session.commit()
            for item in items:
                order_item:OrderItem= OrderItem(
                    name=item['name'],
                    price=item['price'],
                    quantity=item['quantity'],
                    item_id=item['id'],
                    order_id=order.id
                )
                db.session.add(order_item)
                order.total+=order_item.quantity*order_item.price
                db.session.commit()
            return jsonify(message="order created successfully"),201
        else:
            return jsonify(message="order was not created",error='no items passed'),400
        
    except Exception as error:
        return jsonify(error=str(error.args),messsage="error occured when creating order")


@orders.route("/add",methods=['POST','GET'])
@login_required
def orders_add_route():
    business:Business=Business.query.get(current_user.business_id)
    date=datetime.today().replace(minute=0,hour=0,microsecond=0)
    count=Order.query.filter(Order.business_id==current_user.business_id,Order.created_at>=date).count()
    if count >= business.max_orders:
        flash('you have reached the maximum number of orders for today. upgrade for to increase your limit!')
        return redirect(request.referrer)
    if request.method == 'POST':
        customer=request.form.get('customer')
        contact=request.form.get('contact')
        address=request.form.get('address')
        delivery_date=request.form.get('delivery_date')
        if not(delivery_date == None or delivery_date == ''):
            if ( datetime.strptime(delivery_date,'%Y-%m-%d') < datetime.now()):
                flash("delivery date given is passed ! we have set it to null please open the order and  update")
                delivery_date=None
        else:
            delivery_date=None
        business.today_orders=count+1
        db.session.add(Order(customer,contact,address,0,delivery_date,current_user.business_id))
        db.session.commit()
    return redirect('/orders')

@orders.route("/<id>",methods=['POST','GET'])
@login_required
def order_route(id):
 
    order:Order= Order.query.filter(Order.id==id,Order.sold ==False,Order.business_id==current_user.business_id).first()
    if order == None:
        return redirect('/orders')
    
    if request.method == 'POST':
        try:
            name=request.form.get('name')
            quantity=request.form.get('quantity')
            price=request.form.get('price')
            item_id=request.form.get('item_id')
            vat=float(request.form.get('vat'))
            if vat != 0:
                vat=(vat*float(price))/100
            db.session.add(OrderItem(name,price,quantity,item_id,vat=vat,order_id=order.id))
            order.total+=float(price)*int(quantity)
            order.vat=round(order.vat+vat*int(quantity),2)
            order.updated_at=datetime.now()
            db.session.commit()
            return redirect(request.referrer)
        except Exception as error:
            print(str(error.args))
            flash("an error occurred try update the item details !")
    search=request.args.get('search')
    if search==None:
        search=''

    items=Item.query.filter(Item.business_id==current_user.business_id,Item.active,Item.name.like(f"%{search}%")
                            ).order_by(Item.id.asc()).all()
    order_items=OrderItem.query.filter_by(order_id=order.id).all()
    return render_template("order_page.html",order=order,order_items=order_items,items=items,search=search)

@orders.route("/<id>/<itemid>")
@login_required
def remove_item_route(id,itemid):
    try:
        order:Order= Order.query.filter(Order.id==id,Order.sold ==False,Order.business_id==current_user.business_id).first()
        if order == None:
            return redirect('/orders')
        item:OrderItem=OrderItem.query.filter_by(id=itemid).first()
        if item ==None:
            return redirect('/orders')
        order.total-=item.price*item.quantity
        order.vat=round(order.vat-item.vat*item.quantity,2)
        order.updated_at=datetime.now()
        db.session.delete(item)
        db.session.commit()
    except Exception as error:
        print(str(error.args))
        flash("an error occurred during the process !!")
    return redirect(request.referrer)

@orders.route("/<id>/update",methods=['POST','GET'])
@login_required
def order_update_route(id):
    try:
        order:Order= Order.query.filter(Order.id==id,Order.sold ==False,Order.business_id==current_user.business_id).first()
        if order == None :
            return redirect(request.referrer)
        if request.method =='POST':
            order.customer=request.form.get('customer')
            order.contact=request.form.get('contact')
            order.address=request.form.get('address')
            delivery_date=request.form.get('delivery_date')
            if delivery_date != None and delivery_date != '':
                if datetime.strptime(delivery_date,'%Y-%m-%d').date() < datetime.now().date():
                    flash("delivery date given is past today!")
                else:
                    order.delivery_date=delivery_date
        
            db.session.commit()
    except Exception as error:
        print(error.args)
        flash('error updating order')    
    
    return redirect(f"/orders/{id}")


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
        ).order_by(Order.id.asc()).all()
    
    return render_template("sales.html",orders=business_sales,date=date.date())

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