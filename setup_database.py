#!/usr/bin/env python3
"""
Database setup script for CRM application
Creates tables and populates with sample data
"""

import os
import sys
from datetime import datetime, timedelta
from decimal import Decimal

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db, User, Customer, Product, Order, OrderItem, Contact

def setup_database():
    app = create_app()
    
    with app.app_context():
        # Create all tables
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
            print("✓ Admin user created: admin@crm.local / admin123")
        
        # Create sample customers if none exist
        if Customer.query.count() == 0:
            customers = [
                Customer(first_name='Anna', last_name='Berger', email='anna.berger@example.com', phone='+43 123 456789'),
                Customer(first_name='Max', last_name='Haber', email='max.huber@example.com', phone='+43 987 654321'),
                Customer(first_name='Lisa', last_name='Müller', email='lisa.mueller@example.com', phone='+43 555 123456'),
                Customer(first_name='Thomas', last_name='Schmidt', email='thomas.schmidt@example.com', phone='+43 777 888999'),
                Customer(first_name='Sarah', last_name='Wagner', email='sarah.wagner@example.com', phone='+43 111 222333'),
            ]
            
            for customer in customers:
                db.session.add(customer)
            db.session.commit()
            print(f"✓ Created {len(customers)} sample customers")
        
        # Create sample products if none exist
        if Product.query.count() == 0:
            products = [
                Product(sku='PROD-001', name='Software Lizenz Basic', base_price=Decimal('99.00')),
                Product(sku='PROD-002', name='Software Lizenz Pro', base_price=Decimal('199.00')),
                Product(sku='PROD-003', name='Support Paket', base_price=Decimal('49.00')),
                Product(sku='PROD-004', name='Consulting Stunde', base_price=Decimal('120.00')),
                Product(sku='PROD-005', name='Training Paket', base_price=Decimal('299.00')),
            ]
            
            for product in products:
                db.session.add(product)
            db.session.commit()
            print(f"✓ Created {len(products)} sample products")
        
        # Create sample orders if none exist
        if Order.query.count() == 0:
            customers = Customer.query.all()
            products = Product.query.all()
            
            for i, customer in enumerate(customers):
                # Create 1-3 orders per customer
                for j in range(1, 4):
                    order_date = datetime.now() - timedelta(days=i*10 + j*5)
                    order = Order(
                        customer_id=customer.id,
                        order_date=order_date,
                        status='Bezahlt' if j % 2 == 0 else 'Offen',
                        total_amount=Decimal('0')
                    )
                    db.session.add(order)
                    db.session.flush()  # Get the order ID
                    
                    # Add 1-2 items per order
                    total = Decimal('0')
                    for k in range(1, 3):
                        product = products[(i + j + k) % len(products)]
                        quantity = (i + j + k) % 3 + 1
                        item_total = product.base_price * quantity
                        
                        order_item = OrderItem(
                            order_id=order.id,
                            product_id=product.id,
                            quantity=quantity,
                            unit_price=product.base_price
                        )
                        db.session.add(order_item)
                        total += item_total
                    
                    order.total_amount = total
            
            db.session.commit()
            print(f"✓ Created sample orders")
        
        # Create sample contacts if none exist
        if Contact.query.count() == 0:
            customers = Customer.query.all()
            channels = ['Telefon', 'E-Mail', 'Meeting', 'Chat']
            subjects = [
                'Angebot Nachfrage',
                'Terminvereinbarung',
                'Support Anfrage',
                'Rückruf erbeten',
                'Vertragsverlängerung',
                'Neue Funktionen',
                'Schulungstermin',
                'Rechnungsfrage'
            ]
            
            for i, customer in enumerate(customers):
                for j in range(2, 5):  # 2-4 contacts per customer
                    contact_time = datetime.now() - timedelta(days=i*5 + j*2)
                    channel = channels[(i + j) % len(channels)]
                    subject = subjects[(i + j) % len(subjects)]
                    
                    contact = Contact(
                        customer_id=customer.id,
                        user_id=admin.id,
                        channel=channel,
                        subject=subject,
                        notes=f'Dies ist eine Beispiel-Notiz für den Kontakt am {contact_time.strftime("%d.%m.%Y")}.',
                        contact_time=contact_time
                    )
                    db.session.add(contact)
            
            db.session.commit()
            print(f"✓ Created sample contacts")
        
        print("\n🎉 Database setup completed successfully!")
        print("You can now start the Flask application with: python app.py")

if __name__ == '__main__':
    setup_database()