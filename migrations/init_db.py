"""
Datenbank-Initialisierung und Seeder für CRM
Erstellt alle Tabellen und fügt Beispieldaten ein
"""

from app import app
from models import db, Customer, Order, OrderItem, Product, Contact, User
from datetime import datetime, timedelta
import random

def init_database():
    """Erstellt alle Tabellen"""
    with app.app_context():
        print("Erstelle Datenbanktabellen...")
        db.create_all()
        print("✓ Tabellen erfolgreich erstellt!")

def seed_data():
    """Fügt Beispieldaten ein (≥10 Kunden, 50 Bestellungen, 50 Kontakte)"""
    with app.app_context():
        # Prüfe ob bereits Daten vorhanden sind
        if Customer.query.first():
            print("Datenbank enthält bereits Daten. Überspringe Seeding.")
            return
        
        print("Füge Beispieldaten ein...")
        
        # 1. Benutzer erstellen
        users = [
            User(name="Sarah König", email="s.koenig@crm.com", role="Lehrer"),
            User(name="Lars Graf", email="l.graf@crm.com", role="Schüler"),
            User(name="Maria Weber", email="m.weber@crm.com", role="Admin"),
            User(name="Thomas Müller", email="t.mueller@crm.com", role="Schüler"),
        ]
        db.session.add_all(users)
        db.session.commit()
        print(f"✓ {len(users)} Benutzer erstellt")
        
        # 2. Produkte erstellen
        products = [
            Product(sku="PRD-001", name="Premium Laptop", base_price=1299.00),
            Product(sku="PRD-002", name="Wireless Mouse", base_price=29.99),
            Product(sku="PRD-003", name="Mechanical Keyboard", base_price=149.00),
            Product(sku="PRD-004", name="27\" Monitor", base_price=399.00),
            Product(sku="PRD-005", name="USB-C Hub", base_price=79.00),
            Product(sku="PRD-006", name="Webcam HD", base_price=89.00),
            Product(sku="PRD-007", name="Headset Pro", base_price=199.00),
            Product(sku="PRD-008", name="Desk Lamp LED", base_price=45.00),
            Product(sku="PRD-009", name="Ergonomic Chair", base_price=449.00),
            Product(sku="PRD-010", name="Standing Desk", base_price=699.00),
        ]
        db.session.add_all(products)
        db.session.commit()
        print(f"✓ {len(products)} Produkte erstellt")
        
        # 3. Kunden erstellen (mind. 10)
        customers_data = [
            {"first_name": "Anna", "last_name": "Berger", "email": "anna.berger@email.com", "phone": "+43 664 1234567"},
            {"first_name": "Max", "last_name": "Huber", "email": "max.huber@email.com", "phone": "+43 664 2345678"},
            {"first_name": "Julia", "last_name": "Schmidt", "email": "julia.schmidt@email.com", "phone": "+43 664 3456789"},
            {"first_name": "Thomas", "last_name": "Bauer", "email": "thomas.bauer@email.com", "phone": "+43 664 4567890"},
            {"first_name": "Laura", "last_name": "Wagner", "email": "laura.wagner@email.com", "phone": "+43 664 5678901"},
            {"first_name": "Michael", "last_name": "Gruber", "email": "michael.gruber@email.com", "phone": "+43 664 6789012"},
            {"first_name": "Sophie", "last_name": "Müller", "email": "sophie.mueller@email.com", "phone": "+43 664 7890123"},
            {"first_name": "David", "last_name": "Steiner", "email": "david.steiner@email.com", "phone": "+43 664 8901234"},
            {"first_name": "Emma", "last_name": "Koch", "email": "emma.koch@email.com", "phone": "+43 664 9012345"},
            {"first_name": "Lukas", "last_name": "Maier", "email": "lukas.maier@email.com", "phone": "+43 664 0123456"},
            {"first_name": "Sarah", "last_name": "Wolf", "email": "sarah.wolf@email.com", "phone": "+43 664 1122334"},
            {"first_name": "Felix", "last_name": "Schwarz", "email": "felix.schwarz@email.com", "phone": "+43 664 2233445"},
            {"first_name": "Lisa", "last_name": "Becker", "email": "lisa.becker@email.com", "phone": "+43 664 3344556"},
            {"first_name": "Daniel", "last_name": "Hoffmann", "email": "daniel.hoffmann@email.com", "phone": "+43 664 4455667"},
            {"first_name": "Nina", "last_name": "Richter", "email": "nina.richter@email.com", "phone": "+43 664 5566778"},
        ]
        
        customers = [Customer(**data) for data in customers_data]
        db.session.add_all(customers)
        db.session.commit()
        print(f"✓ {len(customers)} Kunden erstellt")
        
        # 4. Bestellungen erstellen (mind. 50)
        statuses = ['Offen', 'Bezahlt', 'Storniert']
        base_date = datetime.now()
        
        orders = []
        for i in range(60):
            customer = random.choice(customers)
            days_ago = random.randint(1, 365)
            order_date = base_date - timedelta(days=days_ago)
            
            # Zufällige Anzahl von Produkten (1-4)
            num_items = random.randint(1, 4)
            selected_products = random.sample(products, num_items)
            
            # Berechne Gesamtsumme
            total = sum(p.base_price * random.randint(1, 3) for p in selected_products)
            
            order = Order(
                customer_id=customer.id,
                order_date=order_date,
                status=random.choice(statuses),
                total_amount=total
            )
            orders.append(order)
        
        db.session.add_all(orders)
        db.session.commit()
        print(f"✓ {len(orders)} Bestellungen erstellt")
        
        # 5. Bestellpositionen erstellen
        order_items = []
        for order in orders:
            num_items = random.randint(1, 4)
            selected_products = random.sample(products, num_items)
            
            for product in selected_products:
                quantity = random.randint(1, 3)
                item = OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=quantity,
                    unit_price=product.base_price
                )
                order_items.append(item)
        
        db.session.add_all(order_items)
        db.session.commit()
        print(f"✓ {len(order_items)} Bestellpositionen erstellt")
        
        # 6. Kontakte erstellen (mind. 50)
        channels = ['Telefon', 'E-Mail', 'Meeting', 'Chat']
        subjects = [
            "Angebot angefragt",
            "Nachfrage zum Liefertermin",
            "Rückruf erbeten",
            "Produktberatung",
            "Reklamation",
            "Feedback zur Bestellung",
            "Terminvereinbarung",
            "Technischer Support",
            "Preisanfrage",
            "Statusupdate gewünscht"
        ]
        
        contacts = []
        for i in range(70):
            customer = random.choice(customers)
            user = random.choice(users)
            days_ago = random.randint(1, 180)
            contact_time = base_date - timedelta(days=days_ago, hours=random.randint(8, 18))
            
            contact = Contact(
                customer_id=customer.id,
                user_id=user.id,
                channel=random.choice(channels),
                subject=random.choice(subjects),
                notes=f"Notiz zum Kontakt #{i+1}",
                contact_time=contact_time
            )
            contacts.append(contact)
        
        db.session.add_all(contacts)
        db.session.commit()
        print(f"✓ {len(contacts)} Kontakte erstellt")
        
        print("\n✓ Datenbank erfolgreich initialisiert und mit Beispieldaten gefüllt!")
        print(f"  - {len(users)} Benutzer")
        print(f"  - {len(products)} Produkte")
        print(f"  - {len(customers)} Kunden")
        print(f"  - {len(orders)} Bestellungen")
        print(f"  - {len(order_items)} Bestellpositionen")
        print(f"  - {len(contacts)} Kontakte")

if __name__ == "__main__":
    print("=== CRM Datenbank-Initialisierung ===\n")
    
    # Tabellen erstellen
    init_database()
    
    # Beispieldaten einfügen
    seed_data()
    
    print("\n=== Initialisierung abgeschlossen ===")