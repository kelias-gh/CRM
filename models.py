from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=True)
    password_hash = db.Column(db.String(255))
    role = db.Column(db.Enum('Schüler', 'Lehrer', 'Admin', name='user_role'), default='Schüler')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    contacts = db.relationship('Contact', backref='user', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Customer(db.Model):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True)
    phone = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    orders = db.relationship('Order', backref='customer', lazy='dynamic', cascade='all, delete-orphan')
    contacts = db.relationship('Contact', backref='customer', lazy='dynamic', cascade='all, delete-orphan')
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def total_revenue(self):
        return db.session.query(db.func.sum(Order.total_amount)).filter(
            Order.customer_id == self.id,
            Order.status != 'Storniert'
        ).scalar() or 0
    
    @property
    def last_year_revenue(self):
        current_year = datetime.now().year
        return db.session.query(db.func.sum(Order.total_amount)).filter(
            Order.customer_id == self.id,
            Order.status != 'Storniert',
            db.extract('year', Order.order_date) == current_year - 1
        ).scalar() or 0
    
    @property
    def last_contact(self):
        return Contact.query.filter_by(customer_id=self.id).order_by(
            Contact.contact_time.desc()
        ).first()
    
    @property
    def last_contact_days(self):
        if self.last_contact:
            return (datetime.now() - self.last_contact.contact_time).days
        return None

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(255), nullable=False)
    base_price = db.Column(db.Numeric(10, 2), nullable=False)
    
    order_items = db.relationship('OrderItem', backref='product', lazy='dynamic')

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.Enum('Offen', 'Bezahlt', 'Storniert', name='order_status'), default='Offen')
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    
    order_items = db.relationship('OrderItem', backref='order', lazy='dynamic', cascade='all, delete-orphan')
    
    __table_args__ = (
        db.Index('idx_orders_date', 'order_date'),
        db.Index('idx_orders_customer_date', 'customer_id', 'order_date'),
    )

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)

class Contact(db.Model):
    __tablename__ = 'contacts'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    channel = db.Column(db.Enum('Telefon', 'E-Mail', 'Meeting', 'Chat', name='contact_channel'), nullable=False)
    subject = db.Column(db.String(255))
    notes = db.Column(db.Text)
    contact_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    __table_args__ = (
        db.Index('idx_contacts_time', 'contact_time'),
        db.Index('idx_contacts_customer_time', 'customer_id', 'contact_time'),
    )