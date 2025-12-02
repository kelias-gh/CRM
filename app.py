from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, login_required, current_user
from datetime import datetime, timedelta
from decimal import Decimal
import os

from config import Config
from models import db, User, Customer, Product, Order, OrderItem, Contact

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    with app.app_context():
        db.create_all()
        
        # Create default admin user if not exists
        admin = User.query.filter_by(email='admin@crm.local').first()
        if not admin:
            admin = User(
                name='Admin User',
                email='admin@crm.local',
                role='Admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
    
    @app.route('/')
    @login_required
    def index():
        # Get search parameters
        customer_search = request.args.get('customer_search', '')
        order_search = request.args.get('order_search', '')
        contact_filter = request.args.get('contact_filter', '')
        
        # Query customers
        customer_query = Customer.query
        if customer_search:
            customer_query = customer_query.filter(
                db.or_(
                    Customer.first_name.ilike(f'%{customer_search}%'),
                    Customer.last_name.ilike(f'%{customer_search}%'),
                    Customer.email.ilike(f'%{customer_search}%'),
                    Customer.phone.ilike(f'%{customer_search}%')
                )
            )
        customers = customer_query.order_by(Customer.last_name, Customer.first_name).limit(20).all()
        
        # Query orders (global, chronological)
        order_query = db.session.query(Order, Customer).join(Customer)
        if order_search:
            order_query = order_query.filter(
                db.or_(
                    Order.id.ilike(f'%{order_search}%'),
                    Customer.first_name.ilike(f'%{order_search}%'),
                    Customer.last_name.ilike(f'%{order_search}%')
                )
            )
        orders = order_query.order_by(Order.order_date.desc()).limit(50).all()
        
        # Query contacts (global, chronological, filterable)
        contact_query = db.session.query(Contact, Customer).join(Customer)
        if contact_filter:
            contact_query = contact_query.filter(Contact.channel == contact_filter)
        contacts = contact_query.order_by(Contact.contact_time.desc()).limit(50).all()
        
        return render_template('index.html',
                             customers=customers,
                             orders=orders,
                             contacts=contacts,
                             customer_search=customer_search,
                             order_search=order_search,
                             contact_filter=contact_filter)
    
    @app.route('/customer/<int:customer_id>')
    @login_required
    def customer_detail(customer_id):
        customer = Customer.query.get_or_404(customer_id)
        
        # Get date range parameters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # Query orders for this customer
        order_query = Order.query.filter_by(customer_id=customer_id)
        
        # Apply date range filter if provided
        if start_date and end_date:
            try:
                start_dt = datetime.strptime(start_date, '%Y-%m-%d')
                end_dt = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
                order_query = order_query.filter(
                    Order.order_date.between(start_dt, end_dt)
                )
            except ValueError:
                flash('Invalid date format', 'error')
        
        orders = order_query.order_by(Order.order_date.desc()).all()
        
        # Calculate revenue for filtered period
        if start_date and end_date:
            period_revenue = db.session.query(db.func.sum(Order.total_amount)).filter(
                Order.customer_id == customer_id,
                Order.status != 'Storniert',
                Order.order_date.between(start_dt, end_dt)
            ).scalar() or 0
        else:
            period_revenue = customer.total_revenue
        
        # Get contacts for this customer
        contacts = Contact.query.filter_by(customer_id=customer_id).order_by(
            Contact.contact_time.desc()
        ).all()
        
        return render_template('customer_detail.html',
                             customer=customer,
                             orders=orders,
                             contacts=contacts,
                             period_revenue=period_revenue,
                             start_date=start_date,
                             end_date=end_date)
    
    @app.route('/customer/<int:customer_id>/edit', methods=['GET', 'POST'])
    @login_required
    def edit_customer(customer_id):
        customer = Customer.query.get_or_404(customer_id)
        
        if request.method == 'POST':
            # Update customer information
            customer.first_name = request.form['first_name'].strip()
            customer.last_name = request.form['last_name'].strip()
            customer.email = request.form['email'].strip() or None
            customer.phone = request.form['phone'].strip() or None
            
            try:
                db.session.commit()
                flash('Customer information updated successfully!', 'success')
                return redirect(url_for('customer_detail', customer_id=customer.id))
            except Exception as e:
                db.session.rollback()
                flash('Error updating customer information.', 'error')
        
        return render_template('edit_customer.html', customer=customer)
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            user = User.query.filter_by(email=email).first()
            
            if user and user.check_password(password):
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash('Invalid email or password', 'error')
        
        return render_template('login.html')
    
    @app.route('/api/customers/search')
    @login_required
    def api_customers_search():
        query = request.args.get('q', '')
        customers = Customer.query.filter(
            db.or_(
                Customer.first_name.ilike(f'%{query}%'),
                Customer.last_name.ilike(f'%{query}%'),
                Customer.email.ilike(f'%{query}%')
            )
        ).limit(10).all()
        
        return jsonify([{
            'id': c.id,
            'name': c.full_name,
            'email': c.email,
            'phone': c.phone
        } for c in customers])
    
    @app.route('/api/orders/search')
    @login_required
    def api_orders_search():
        query = request.args.get('q', '')
        orders = db.session.query(Order, Customer).join(Customer).filter(
            db.or_(
                Order.id.ilike(f'%{query}%'),
                Customer.first_name.ilike(f'%{query}%'),
                Customer.last_name.ilike(f'%{query}%')
            )
        ).order_by(Order.order_date.desc()).limit(10).all()
        
        return jsonify([{
            'id': o.Order.id,
            'date': o.Order.order_date.isoformat(),
            'customer': o.Customer.full_name,
            'total': float(o.Order.total_amount),
            'status': o.Order.status
        } for o in orders])
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)