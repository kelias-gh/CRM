from flask import Blueprint, render_template, request, jsonify
from models import db, Contact, Customer
from sqlalchemy import func

contacts_bp = Blueprint('contacts', __name__, url_prefix='/contacts')

@contacts_bp.route('/')
def list_contacts():
    """Globale Kontaktübersicht (neueste zuerst, filterbar nach Art)"""
    channel_filter = request.args.get('channel', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = 50
    
    # Basis-Query
    base_query = db.session.query(
        Contact.contact_time,
        Contact.channel,
        Contact.subject,
        func.concat(Customer.last_name, ', ', Customer.first_name).label('customer_name'),
        Customer.id.label('customer_id')
    ).join(Customer)
    
    # Filter nach Kanal
    if channel_filter and channel_filter in ['Telefon', 'E-Mail', 'Meeting', 'Chat']:
        base_query = base_query.filter(Contact.channel == channel_filter)
    
    # Sortierung und Pagination
    contacts = base_query.order_by(Contact.contact_time.desc())\
        .limit(per_page).offset((page - 1) * per_page).all()
    
    # Gesamtanzahl für Pagination
    total = base_query.count()
    has_next = (page * per_page) < total
    has_prev = page > 1
    
    return render_template('contacts_list.html',
                         contacts=contacts,
                         channel_filter=channel_filter,
                         page=page,
                         has_next=has_next,
                         has_prev=has_prev)