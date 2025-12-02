from flask import Flask, render_template, request, jsonify
from models import db, Customer, Order, OrderItem, Product, Contact, User
from views.customers import customers_bp
from views.orders import orders_bp
from views.contacts import contacts_bp
import os
from datetime import datetime, timedelta
from sqlalchemy import func, extract

app = Flask(__name__)

# Konfiguration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'mysql+pymysql://username:password@username.mysql.pythonanywhere-services.com/username$crm_db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_recycle': 280,
    'pool_pre_ping': True
}

# Initialisiere Datenbank
db.init_app(app)

# Registriere Blueprints
app.register_blueprint(customers_bp)
app.register_blueprint(orders_bp)
app.register_blueprint(contacts_bp)

@app.route('/')
def index():
    """Startseite mit drei Übersichten"""
    # Kundenliste (erste 10)
    customers = Customer.query.order_by(Customer.last_name, Customer.first_name).limit(10).all()
    
    # Globale Bestellungen (neueste zuerst, erste 10)
    orders = db.session.query(
        Order.id,
        Order.order_date,
        Order.total_amount,
        Order.status,
        func.concat(Customer.last_name, ', ', Customer.first_name).label('customer_name')
    ).join(Customer).order_by(Order.order_date.desc()).limit(10).all()
    
    # Globale Kontakte (neueste zuerst, erste 10)
    contacts = db.session.query(
        Contact.contact_time,
        Contact.channel,
        Contact.subject,
        func.concat(Customer.last_name, ', ', Customer.first_name).label('customer_name')
    ).join(Customer).order_by(Contact.contact_time.desc()).limit(10).all()
    
    return render_template('index.html', 
                         customers=customers,
                         orders=orders,
                         contacts=contacts)

@app.route('/health')
def health():
    """Healthcheck für PythonAnywhere"""
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True)