from flask import Blueprint, render_template, request, jsonify
from models import db, Order, Customer
from sqlalchemy import func

orders_bp = Blueprint('orders', __name__, url_prefix='/orders')

@orders_bp.route('/')
def list_orders():
    """Globale Bestellübersicht (neueste zuerst)"""
    query = request.args.get('q', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = 50
    
    # Basis-Query
    base_query = db.session.query(
        Order.id,
        Order.order_date,
        Order.total_amount,
        Order.status,
        func.concat(Customer.last_name, ', ', Customer.first_name).label('customer_name'),
        Customer.id.label('customer_id')
    ).join(Customer)
    
    # Suche nach Bestellnummer oder Kundenname
    if query:
        search = f"%{query}%"
        base_query = base_query.filter(
            db.or_(
                func.cast(Order.id, db.String).like(search),
                Customer.first_name.like(search),
                Customer.last_name.like(search)
            )
        )
    
    # Sortierung und Pagination
    orders = base_query.order_by(Order.order_date.desc())\
        .limit(per_page).offset((page - 1) * per_page).all()
    
    # Gesamtanzahl für Pagination
    total = base_query.count()
    has_next = (page * per_page) < total
    has_prev = page > 1
    
    return render_template('orders_list.html',
                         orders=orders,
                         query=query,
                         page=page,
                         has_next=has_next,
                         has_prev=has_prev)