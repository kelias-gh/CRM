from flask import Blueprint, render_template, request, jsonify
from models import db, Customer, Order, Contact
from sqlalchemy import func, extract, and_
from datetime import datetime, timedelta

customers_bp = Blueprint('customers', __name__, url_prefix='/customers')

@customers_bp.route('/')
def list_customers():
    """Kundenliste mit Suche"""
    query = request.args.get('q', '').strip()
    
    if query:
        search = f"%{query}%"
        customers = Customer.query.filter(
            db.or_(
                Customer.first_name.like(search),
                Customer.last_name.like(search),
                Customer.email.like(search),
                Customer.phone.like(search)
            )
        ).order_by(Customer.last_name, Customer.first_name).limit(50).all()
    else:
        customers = Customer.query.order_by(
            Customer.last_name, Customer.first_name
        ).limit(50).all()
    
    # Letzten Kontakt für jeden Kunden ermitteln
    customer_data = []
    for customer in customers:
        last_contact = Contact.query.filter_by(customer_id=customer.id)\
            .order_by(Contact.contact_time.desc()).first()
        
        customer_data.append({
            'customer': customer,
            'last_contact': last_contact
        })
    
    return render_template('customers_list.html', 
                         customer_data=customer_data,
                         query=query)

@customers_bp.route('/<int:customer_id>')
def customer_detail(customer_id):
    """Kunden-Detailansicht mit KPIs"""
    customer = Customer.query.get_or_404(customer_id)
    
    # KPI: Umsatz gesamt
    total_revenue = db.session.query(func.sum(Order.total_amount))\
        .filter(Order.customer_id == customer_id).scalar() or 0
    
    # KPI: Umsatz letztes Kalenderjahr
    current_year = datetime.now().year
    last_year_start = datetime(current_year - 1, 1, 1)
    last_year_end = datetime(current_year, 1, 1)
    
    last_year_revenue = db.session.query(func.sum(Order.total_amount))\
        .filter(
            Order.customer_id == customer_id,
            Order.order_date >= last_year_start,
            Order.order_date < last_year_end
        ).scalar() or 0
    
    # Datumsbereich aus Query-Parametern
    date_from = request.args.get('from')
    date_to = request.args.get('to')
    range_revenue = None
    
    if date_from and date_to:
        try:
            date_from_obj = datetime.strptime(date_from, '%Y-%m-%d')
            date_to_obj = datetime.strptime(date_to, '%Y-%m-%d')
            
            range_revenue = db.session.query(func.sum(Order.total_amount))\
                .filter(
                    Order.customer_id == customer_id,
                    Order.order_date >= date_from_obj,
                    Order.order_date <= date_to_obj
                ).scalar() or 0
        except ValueError:
            pass
    
    # Letzte Bestellungen (neueste zuerst)
    recent_orders = Order.query.filter_by(customer_id=customer_id)\
        .order_by(Order.order_date.desc()).limit(10).all()
    
    # Anzahl Positionen pro Bestellung
    orders_with_items = []
    for order in recent_orders:
        item_count = db.session.query(func.count(db.distinct(db.text('order_items.id'))))\
            .filter(db.text('order_items.order_id = :order_id'))\
            .params(order_id=order.id).scalar() or 0
        orders_with_items.append({
            'order': order,
            'item_count': item_count
        })
    
    # Letzte Kontakte (neueste zuerst)
    recent_contacts = Contact.query.filter_by(customer_id=customer_id)\
        .order_by(Contact.contact_time.desc()).limit(10).all()
    
    # Letzter Kontakt für Header
    last_contact = recent_contacts[0] if recent_contacts else None
    
    return render_template('customer_detail.html',
                         customer=customer,
                         total_revenue=float(total_revenue),
                         last_year_revenue=float(last_year_revenue),
                         range_revenue=float(range_revenue) if range_revenue is not None else None,
                         date_from=date_from,
                         date_to=date_to,
                         orders_with_items=orders_with_items,
                         recent_contacts=recent_contacts,
                         last_contact=last_contact)

@customers_bp.route('/<int:customer_id>/revenue')
def customer_revenue(customer_id):
    """API-Endpoint für Umsatzfilter"""
    date_from = request.args.get('from')
    date_to = request.args.get('to')
    
    if not date_from or not date_to:
        return jsonify({'error': 'from and to parameters required'}), 400
    
    try:
        date_from_obj = datetime.strptime(date_from, '%Y-%m-%d')
        date_to_obj = datetime.strptime(date_to, '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    
    revenue = db.session.query(func.sum(Order.total_amount))\
        .filter(
            Order.customer_id == customer_id,
            Order.order_date >= date_from_obj,
            Order.order_date <= date_to_obj
        ).scalar() or 0
    
    return jsonify({
        'customer_id': customer_id,
        'from': date_from,
        'to': date_to,
        'revenue': float(revenue)
    })