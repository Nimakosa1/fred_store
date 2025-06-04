from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse, Response
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, date
import json
from fastapi_mcp import FastApiMCP
from fastapi.responses import StreamingResponse

from database import engine, get_db
import models
import db_models
from db_models import User, Product, Order, OrderItem, Subscription

# Create database tables
db_models.Base.metadata.create_all(bind=engine)

class PrettyJSONResponse(JSONResponse):
    def render(self, content) -> bytes:
        return json.dumps(
            jsonable_encoder(content),
            ensure_ascii=False,
            allow_nan=False,
            indent=2,
            separators=(", ", ": "),
        ).encode("utf-8")

app = FastAPI(
    title="Fred's Store API",
    default_response_class=PrettyJSONResponse
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize MCP with custom name and proper configuration
mcp = FastApiMCP(
    app,
    name="Fred's Store MCP Server",
    describe_all_responses=True,
    describe_full_response_schema=True
)

# Mount the MCP server
mcp.mount()

@app.get("/")
def read_root():
    return {"message": "WELCOME TO FRED'S STORE"}

# Product routes with proper documentation
@app.get("/products", response_model=List[models.Product], tags=["products"])
def get_products(db: Session = Depends(get_db)):
    """List all available products in the store"""
    return db.query(Product).all()

@app.get("/products/{product_id}", response_model=models.Product, tags=["products"])
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get details of a specific product by its ID"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/products", response_model=models.Product, tags=["products"])
def create_product(product: models.ProductCreate, db: Session = Depends(get_db)):
    """Create a new product in the store"""
    db_product = Product(**product.model_dump())
    db_product.release_date = date.today()
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.put("/products/{product_id}", response_model=models.Product)
def update_product(product_id: int, product: models.ProductCreate, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    for key, value in product.model_dump().items():
        setattr(db_product, key, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}

# User routes
@app.get("/users", response_model=List[models.User])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@app.get("/users/{user_id}", response_model=models.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users", response_model=models.User)
def create_user(user: models.UserCreate, db: Session = Depends(get_db)):
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.put("/users/{user_id}", response_model=models.User)
def update_user(user_id: int, user: models.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    for key, value in user.model_dump().items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

# Order routes
@app.get("/orders", response_model=List[models.Order])
def get_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()

@app.get("/orders/{order_id}", response_model=models.Order)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.post("/orders", response_model=models.Order)
def create_order(order: models.OrderCreate, db: Session = Depends(get_db)):
    # Create order
    db_order = Order(
        user_id=order.user_id,
        status=order.status,
        total_amount=order.total_amount
    )
    db.add(db_order)
    db.flush()  # Get order ID without committing
    
    # Create order items
    for item in order.items:
        db_item = OrderItem(
            order_id=db_order.id,
            **item.model_dump()
        )
        db.add(db_item)
    
    db.commit()
    db.refresh(db_order)
    return db_order

@app.delete("/orders/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    db.delete(order)
    db.commit()
    return {"message": "Order deleted successfully"}

# Subscription routes
@app.get("/subscriptions", response_model=List[models.Subscription])
def get_subscriptions(db: Session = Depends(get_db)):
    return db.query(Subscription).all()

@app.get("/subscriptions/{subscription_id}", response_model=models.Subscription)
def get_subscription(subscription_id: int, db: Session = Depends(get_db)):
    subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return subscription

@app.post("/subscriptions", response_model=models.Subscription)
def create_subscription(subscription: models.SubscriptionCreate, db: Session = Depends(get_db)):
    db_subscription = Subscription(**subscription.model_dump())
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription

@app.put("/subscriptions/{subscription_id}", response_model=models.Subscription)
def update_subscription(subscription_id: int, subscription: models.SubscriptionCreate, db: Session = Depends(get_db)):
    db_subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    if not db_subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    for key, value in subscription.model_dump().items():
        setattr(db_subscription, key, value)
    
    db.commit()
    db.refresh(db_subscription)
    return db_subscription

@app.delete("/subscriptions/{subscription_id}")
def delete_subscription(subscription_id: int, db: Session = Depends(get_db)):
    subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    db.delete(subscription)
    db.commit()
    return {"message": "Subscription deleted successfully"}

# User's Orders and Subscriptions
@app.get("/users/{user_id}/orders", response_model=List[models.Order])
def get_user_orders(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.orders

@app.get("/users/{user_id}/subscriptions", response_model=List[models.Subscription])
def get_user_subscriptions(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.subscriptions 