from datetime import datetime, date, timedelta
import random
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from db_models import User, Product, Order, OrderItem, Subscription

def init_db():
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if data already exists
        if db.query(Product).count() > 0:
            print("Database already initialized")
            return

        # Add products
        products = [
            Product(
                name="Adobe Photoshop",
                description="Professional image editing and manipulation software for photographers, graphic designers, and artists.",
                category="Photo Editing",
                price=20.99,
                subscription=True,
                license_type="Single User",
                version="2024",
                platform="Windows, macOS",
                stock=1000,
                release_date=date(2024, 1, 15),
                is_promoted=True
            ),
            Product(
                name="Adobe Illustrator",
                description="Vector graphics editor and design program for creating logos, icons, drawings, typography, and illustrations.",
                category="Vector Graphics",
                price=20.99,
                subscription=True,
                license_type="Single User",
                version="2024",
                platform="Windows, macOS",
                stock=1000,
                release_date=date(2024, 1, 15),
                is_promoted=True
            ),
            Product(
                name="Adobe Premiere Pro",
                description="Industry-leading video editing software for film, TV, and web content creation.",
                category="Video Editing",
                price=20.99,
                subscription=True,
                license_type="Single User",
                version="2024",
                platform="Windows, macOS",
                stock=1000,
                release_date=date(2024, 1, 15),
                is_promoted=True
            ),
            Product(
                name="Adobe After Effects",
                description="Industry-standard motion graphics and visual effects software.",
                category="Motion Graphics",
                price=20.99,
                subscription=True,
                license_type="Single User",
                version="2024",
                platform="Windows, macOS",
                stock=1000,
                release_date=date(2024, 1, 15),
                is_promoted=False
            ),
            Product(
                name="Adobe Lightroom Classic",
                description="Digital photo workflow and editing software for professional photographers.",
                category="Photo Management",
                price=9.99,
                subscription=True,
                license_type="Single User",
                version="2024",
                platform="Windows, macOS",
                stock=1000,
                release_date=date(2024, 1, 15),
                is_promoted=False
            ),
            Product(
                name="Adobe InDesign",
                description="Page design and layout software for print and digital media.",
                category="Page Layout",
                price=20.99,
                subscription=True,
                license_type="Single User",
                version="2024",
                platform="Windows, macOS",
                stock=1000,
                release_date=date(2024, 1, 15),
                is_promoted=False
            ),
            Product(
                name="Adobe Audition",
                description="Professional audio workstation for mixing, finishing, and precision editing.",
                category="Audio Editing",
                price=20.99,
                subscription=True,
                license_type="Single User",
                version="2024",
                platform="Windows, macOS",
                stock=1000,
                release_date=date(2024, 1, 15),
                is_promoted=False
            ),
            Product(
                name="Adobe Acrobat Pro DC",
                description="Complete PDF solution for working anywhere with documents.",
                category="Document Management",
                price=14.99,
                subscription=True,
                license_type="Single User",
                version="2024",
                platform="Windows, macOS, Web",
                stock=2000,
                release_date=date(2024, 1, 15),
                is_promoted=True
            ),
            Product(
                name="Adobe XD",
                description="UI/UX design tool for creating web and mobile applications.",
                category="UI/UX Design",
                price=9.99,
                subscription=True,
                license_type="Single User",
                version="2024",
                platform="Windows, macOS",
                stock=1000,
                release_date=date(2024, 1, 15),
                is_promoted=False
            ),
            Product(
                name="Adobe Dreamweaver",
                description="Web development tool for designing, coding, and publishing websites.",
                category="Web Development",
                price=20.99,
                subscription=True,
                license_type="Single User",
                version="2024",
                platform="Windows, macOS",
                stock=500,
                release_date=date(2024, 1, 15),
                is_promoted=False
            ),
            Product(
                name="Adobe Animate",
                description="Animation software for creating interactive vector animations.",
                category="Animation",
                price=20.99,
                subscription=True,
                license_type="Single User",
                version="2024",
                platform="Windows, macOS",
                stock=500,
                release_date=date(2024, 1, 15),
                is_promoted=False
            ),
            Product(
                name="Adobe Dimension",
                description="3D design tool for creating photorealistic images.",
                category="3D Design",
                price=20.99,
                subscription=True,
                license_type="Single User",
                version="2024",
                platform="Windows, macOS",
                stock=500,
                release_date=date(2024, 1, 15),
                is_promoted=False
            ),
            Product(
                name="Adobe Substance 3D Stager",
                description="3D scene composition and rendering tool.",
                category="3D Design",
                price=49.99,
                subscription=True,
                license_type="Single User",
                version="2024",
                platform="Windows, macOS",
                stock=300,
                release_date=date(2024, 1, 15),
                is_promoted=True
            ),
            Product(
                name="Adobe Fresco",
                description="Digital painting and drawing app with live brushes.",
                category="Digital Art",
                price=9.99,
                subscription=True,
                license_type="Single User",
                version="2024",
                platform="Windows, iOS",
                stock=1000,
                release_date=date(2024, 1, 15),
                is_promoted=False
            ),
            Product(
                name="Adobe Express",
                description="Quick and easy content creation tool for social media.",
                category="Content Creation",
                price=9.99,
                subscription=True,
                license_type="Single User",
                version="2024",
                platform="Web, iOS, Android",
                stock=5000,
                release_date=date(2024, 1, 15),
                is_promoted=True
            ),
            Product(
                name="Adobe Bridge",
                description="Digital asset management tool for creative professionals.",
                category="Asset Management",
                price=9.99,
                subscription=True,
                license_type="Single User",
                version="2024",
                platform="Windows, macOS",
                stock=500,
                release_date=date(2024, 1, 15),
                is_promoted=False
            ),
            Product(
                name="Adobe Firefly",
                description="AI-powered creative tool for generating and editing images.",
                category="AI Creation",
                price=14.99,
                subscription=True,
                license_type="Single User",
                version="2024",
                platform="Web",
                stock=2000,
                release_date=date(2024, 1, 15),
                is_promoted=True
            ),
            Product(
                name="Adobe Fonts",
                description="Digital font service with thousands of fonts for creative projects.",
                category="Typography",
                price=9.99,
                subscription=True,
                license_type="Single User",
                version="2024",
                platform="Web",
                stock=10000,
                release_date=date(2024, 1, 15),
                is_promoted=False
            ),
            Product(
                name="Adobe Portfolio",
                description="Online portfolio creation tool for creative professionals.",
                category="Web Design",
                price=9.99,
                subscription=True,
                license_type="Single User",
                version="2024",
                platform="Web",
                stock=1000,
                release_date=date(2024, 1, 15),
                is_promoted=False
            ),
            Product(
                name="Adobe Stock",
                description="Royalty-free stock content service with millions of assets.",
                category="Digital Assets",
                price=29.99,
                subscription=True,
                license_type="Single User",
                version="2024",
                platform="Web",
                stock=1000000,
                release_date=date(2024, 1, 15),
                is_promoted=True
            )
        ]
        db.add_all(products)
        db.commit()

        # Add users
        users = [
            User(
                email="sarah.smith@designstudio.com",
                name="Sarah Smith",
                country="United States"
            ),
            User(
                email="john.doe@creativepro.net",
                name="John Doe",
                country="Canada"
            ),
            User(
                email="maria.garcia@digitalarts.es",
                name="Maria Garcia",
                country="Spain"
            ),
            User(
                email="alex.wong@photomaster.com",
                name="Alex Wong",
                country="Singapore"
            ),
            User(
                email="emma.brown@webdev.co.uk",
                name="Emma Brown",
                country="United Kingdom"
            ),
            User(
                email="lucas.mueller@3dartist.de",
                name="Lucas Mueller",
                country="Germany"
            ),
            User(
                email="sophie.dubois@motion.fr",
                name="Sophie Dubois",
                country="France"
            ),
            User(
                email="marco.rossi@studiocreativo.it",
                name="Marco Rossi",
                country="Italy"
            ),
            User(
                email="yuki.tanaka@design.jp",
                name="Yuki Tanaka",
                country="Japan"
            ),
            User(
                email="olivia.wilson@artdirect.com.au",
                name="Olivia Wilson",
                country="Australia"
            ),
            User(
                email="carlos.silva@videomaker.br",
                name="Carlos Silva",
                country="Brazil"
            ),
            User(
                email="anna.kowalski@graphicpro.pl",
                name="Anna Kowalski",
                country="Poland"
            ),
            User(
                email="mohammed.ahmed@creativemena.ae",
                name="Mohammed Ahmed",
                country="United Arab Emirates"
            ),
            User(
                email="lisa.anderson@uxdesign.se",
                name="Lisa Anderson",
                country="Sweden"
            ),
            User(
                email="david.kim@digitalstudio.kr",
                name="David Kim",
                country="South Korea"
            )
        ]
        db.add_all(users)
        db.commit()

        # Add subscriptions
        for user in users:
            num_subscriptions = random.randint(2, 4)
            random_products = random.sample(products, num_subscriptions)
            
            for product in random_products:
                subscription = Subscription(
                    user_id=user.id,
                    product_id=product.id,
                    start_date=date(2024, 1, 1),
                    end_date=date(2024, 12, 31),
                    auto_renew=random.choice([True, True, False])
                )
                db.add(subscription)
        db.commit()

        # Add orders
        for user in users:
            num_orders = random.randint(1, 3)
            for _ in range(num_orders):
                order = Order(
                    user_id=user.id,
                    status=random.choice(["Completed", "Completed", "Completed", "Pending", "Failed"]),
                    created_at=datetime.utcnow() - timedelta(days=random.randint(1, 60)),
                    total_amount=0
                )
                db.add(order)
                db.flush()

                num_items = random.randint(1, 5)
                total_amount = 0
                random_products = random.sample(products, num_items)

                for product in random_products:
                    quantity = random.randint(1, 2)
                    price = product.price
                    total_amount += price * quantity

                    order_item = OrderItem(
                        order_id=order.id,
                        product_id=product.id,
                        quantity=quantity,
                        price_at_purchase=price
                    )
                    db.add(order_item)

                order.total_amount = total_amount
                db.add(order)

        db.commit()
        print("Database initialized successfully")

    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db() 