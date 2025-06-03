from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import random

app = Flask(__name__)

#DATABASE and INITIALIZATION
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///freds_store.db'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#MODELS OF DB
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120))
    country = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Admin fields
    is_admin = db.Column(db.Boolean, default=False)
    admin_role = db.Column(db.String(20), default='user')  # 'user', 'admin', 'super_admin'
    last_login = db.Column(db.DateTime)
    
    # Relationships
    orders = db.relationship('Order', backref='user', lazy=True)
    subscriptions = db.relationship('Subscription', backref='user', lazy=True)
    
    def to_dict(self):
        return {
            'name': self.name,
            'id': self.id,
            'email': self.email,
            'country': self.country,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_admin': self.is_admin,
            'admin_role': self.admin_role,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50))  # e.g. "Pending", "Completed", "Failed"
    total_amount = db.Column(db.Float)
    
    # Relationships
    items = db.relationship('OrderItem', backref='order', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'status': self.status,
            'total_amount': self.total_amount,
            'items': [item.to_dict() for item in self.items]
        }

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    price_at_purchase = db.Column(db.Float)  # in case price changes
    
    # Relationships
    product = db.relationship('Product', backref='order_items', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'price_at_purchase': self.price_at_purchase,
            'product': self.product.to_dict() if self.product else None
        }

class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    auto_renew = db.Column(db.Boolean, default=True)
    
    # Relationships
    product = db.relationship('Product', backref='subscriptions', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'auto_renew': self.auto_renew,
            'product': self.product.to_dict() if self.product else None
        }

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)  # e.g. "Adobe Photoshop"
    description = db.Column(db.Text)
    category = db.Column(db.String(50))  # e.g. "Photo Editing", "Design"
    price = db.Column(db.Float, nullable=False)
    subscription = db.Column(db.Boolean, default=True)  # Is it a recurring subscription?
    license_type = db.Column(db.String(50))  # e.g. "Single User", "Enterprise"
    version = db.Column(db.String(20))  # e.g. "2024"
    platform = db.Column(db.String(50))  # e.g. "Windows", "macOS", "Web"
    stock = db.Column(db.Integer, default=0)  # optional for licensing, but for realism
    release_date = db.Column(db.Date)
    is_promoted = db.Column(db.Boolean, default=False)  # for marketing

    def __repr__(self):
        return f"<Product {self.name} ({self.version}) - {self.category} | ${self.price:.2f} | {self.platform}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'price': self.price,
            'subscription': self.subscription,
            'license_type': self.license_type,
            'version': self.version,
            'platform': self.platform,
            'stock': self.stock,
            'release_date': self.release_date.isoformat() if self.release_date else None,
            'is_promoted': self.is_promoted
        }

#CREATE ALL TABLES
with app.app_context():
    db.create_all()
    
    # Check if products already exist to avoid duplicates
    if Product.query.count() == 0:
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
                release_date=datetime(2024, 1, 15),
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
                release_date=datetime(2024, 1, 15),
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
                release_date=datetime(2024, 1, 15),
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
                release_date=datetime(2024, 1, 15),
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
                release_date=datetime(2024, 1, 15),
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
                release_date=datetime(2024, 1, 15),
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
                release_date=datetime(2024, 1, 15),
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
                release_date=datetime(2024, 1, 15),
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
                release_date=datetime(2024, 1, 15),
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
                release_date=datetime(2024, 1, 15),
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
                release_date=datetime(2024, 1, 15),
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
                release_date=datetime(2024, 1, 15),
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
                release_date=datetime(2024, 1, 15),
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
                release_date=datetime(2024, 1, 15),
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
                release_date=datetime(2024, 1, 15),
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
                release_date=datetime(2024, 1, 15),
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
                release_date=datetime(2024, 1, 15),
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
                release_date=datetime(2024, 1, 15),
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
                release_date=datetime(2024, 1, 15),
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
                release_date=datetime(2024, 1, 15),
                is_promoted=True
            )
        ]
        
        db.session.add_all(products)
        db.session.commit()

    # Add sample users if none exist
    if User.query.count() == 0:
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
        db.session.add_all(users)
        db.session.commit()

        # Create some subscriptions for users
        products = Product.query.all()
        for user in users:
            # Each user gets 2-4 random subscriptions
            num_subscriptions = random.randint(2, 4)
            random_products = random.sample(products, num_subscriptions)
            
            for product in random_products:
                start_date = datetime(2024, 1, 1).date()
                end_date = datetime(2024, 12, 31).date()
                subscription = Subscription(
                    user_id=user.id,
                    product_id=product.id,
                    start_date=start_date,
                    end_date=end_date,
                    auto_renew=random.choice([True, True, False])  # 2/3 chance of auto-renew
                )
                db.session.add(subscription)
        
        db.session.commit()

        # Create some orders for users
        for user in users:
            # Each user gets 1-3 orders
            num_orders = random.randint(1, 3)
            for _ in range(num_orders):
                # Create order
                order = Order(
                    user_id=user.id,
                    status=random.choice(["Completed", "Completed", "Completed", "Pending", "Failed"]),
                    created_at=datetime.utcnow() - timedelta(days=random.randint(1, 60)),
                    total_amount=0  # Will be calculated based on items
                )
                db.session.add(order)
                db.session.flush()  # To get the order ID
                
                # Add 1-5 items to each order
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
                    db.session.add(order_item)
                
                order.total_amount = total_amount
        
        db.session.commit()

#ROUTES
@app.route('/')
def index():
    return jsonify({"message": "WELCOME TO FRED'S STORE"})

@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products])

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    if product:
        return jsonify(product.to_dict())
    else:
        return jsonify({"error": "Product not found"}), 404

@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    new_product = Product(
        name=data['name'],
        description=data['description'],
        category=data['category'],
        price=data['price'],
        subscription=data['subscription'],
        license_type=data['license_type'],
        version=data['version'],
        platform=data['platform'],
        stock=data['stock'],
        release_date=data['release_date'],
        is_promoted=data['is_promoted']
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify(new_product.to_dict()), 201

@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    product = Product.query.get_or_404(product_id)
    if product:
        product.name = data['name']
        product.description = data['description']
        product.category = data['category']
        product.price = data['price']
        product.subscription = data['subscription']
        product.license_type = data['license_type']
        product.version = data['version']
        product.platform = data['platform']
        product.stock = data['stock']
        product.release_date = data['release_date']
        product.is_promoted = data['is_promoted']
        db.session.commit()
        return jsonify(product.to_dict())
    else:
        return jsonify({"error": "Product not found"}), 404

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successfully"}), 200
    else:
        return jsonify({"error": "Product not found"}), 404

# User Routes
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(
        email=data['email'],
        name=data['name'],
        country=data['country']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    user.email = data.get('email', user.email)
    user.name = data.get('name', user.name)
    user.country = data.get('country', user.country)
    db.session.commit()
    return jsonify(user.to_dict())

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"})

# Order Routes
@app.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return jsonify([order.to_dict() for order in orders])

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get_or_404(order_id)
    return jsonify(order.to_dict())

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    new_order = Order(
        user_id=data['user_id'],
        status="Pending",
        total_amount=data['total_amount']
    )
    db.session.add(new_order)
    
    # Create order items
    for item in data['items']:
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=item['product_id'],
            quantity=item['quantity'],
            price_at_purchase=item['price']
        )
        db.session.add(order_item)
    
    db.session.commit()
    return jsonify(new_order.to_dict()), 201

@app.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    order = Order.query.get_or_404(order_id)
    data = request.get_json()
    order.status = data.get('status', order.status)
    order.total_amount = data.get('total_amount', order.total_amount)
    db.session.commit()
    return jsonify(order.to_dict())

@app.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({"message": "Order deleted successfully"})

# Subscription Routes
@app.route('/subscriptions', methods=['GET'])
def get_subscriptions():
    subscriptions = Subscription.query.all()
    return jsonify([sub.to_dict() for sub in subscriptions])

@app.route('/subscriptions/<int:subscription_id>', methods=['GET'])
def get_subscription(subscription_id):
    subscription = Subscription.query.get_or_404(subscription_id)
    return jsonify(subscription.to_dict())

@app.route('/subscriptions', methods=['POST'])
def create_subscription():
    data = request.get_json()
    new_subscription = Subscription(
        user_id=data['user_id'],
        product_id=data['product_id'],
        start_date=datetime.strptime(data['start_date'], '%Y-%m-%d').date(),
        end_date=datetime.strptime(data['end_date'], '%Y-%m-%d').date(),
        auto_renew=data.get('auto_renew', True)
    )
    db.session.add(new_subscription)
    db.session.commit()
    return jsonify(new_subscription.to_dict()), 201

@app.route('/subscriptions/<int:subscription_id>', methods=['PUT'])
def update_subscription(subscription_id):
    subscription = Subscription.query.get_or_404(subscription_id)
    data = request.get_json()
    if 'end_date' in data:
        subscription.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
    if 'auto_renew' in data:
        subscription.auto_renew = data['auto_renew']
    db.session.commit()
    return jsonify(subscription.to_dict())

@app.route('/subscriptions/<int:subscription_id>', methods=['DELETE'])
def delete_subscription(subscription_id):
    subscription = Subscription.query.get_or_404(subscription_id)
    db.session.delete(subscription)
    db.session.commit()
    return jsonify({"message": "Subscription deleted successfully"})

# User's Orders and Subscriptions
@app.route('/users/<int:user_id>/orders', methods=['GET'])
def get_user_orders(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify([order.to_dict() for order in user.orders])

@app.route('/users/<int:user_id>/subscriptions', methods=['GET'])
def get_user_subscriptions(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify([sub.to_dict() for sub in user.subscriptions])

if __name__ == '__main__':
    app.run(debug=True, port=5002)