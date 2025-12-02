from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Customer(db.Model):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True)
    phone = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Beziehungen
    orders = db.relationship('Order', backref='customer', lazy=True, cascade='all, delete-orphan')
    contacts = db.relationship('Contact', backref='customer', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Customer {self.last_name}, {self.first_name}>'
    
    @property
    def full_name(self):
        return f"{self.last_name}, {self.first_name}"

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id', ondelete='CASCADE'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum('Offen', 'Bezahlt', 'Storniert', name='order_status'), default='Offen')
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Beziehungen
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    
    __table_args__ = (
        db.Index('idx_orders_date', 'order_date'),
        db.Index('idx_orders_customer_date', 'customer_id', 'order_date'),
    )
    
    def __repr__(self):
        return f'<Order A-{self.id}>'
    
    @property
    def order_number(self):
        return f"A-{self.id}"

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(255), nullable=False)
    base_price = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Beziehungen
    order_items = db.relationship('OrderItem', backref='product', lazy=True)
    
    def __repr__(self):
        return f'<Product {self.name}>'

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id', ondelete='CASCADE'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    
    def __repr__(self):
        return f'<OrderItem {self.id}>'

class Contact(db.Model):
    __tablename__ = 'contacts'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    channel = db.Column(db.Enum('Telefon', 'E-Mail', 'Meeting', 'Chat', name='contact_channel'), nullable=False)
    subject = db.Column(db.String(255))
    notes = db.Column(db.Text)
    contact_time = db.Column(db.DateTime, nullable=False)
    
    # Beziehungen
    user = db.relationship('User', backref='contacts')
    
    __table_args__ = (
        db.Index('idx_contacts_time', 'contact_time'),
        db.Index('idx_contacts_customer_time', 'customer_id', 'contact_time'),
    )
    
    def __repr__(self):
        return f'<Contact {self.channel} - {self.subject}>'

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True)
    password_hash = db.Column(db.String(255))
    role = db.Column(db.Enum('Schüler', 'Lehrer', 'Admin', name='user_role'), default='Schüler')
    
    def __repr__(self):
        return f'<User {self.name}>'