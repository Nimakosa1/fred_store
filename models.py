from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    price: float
    subscription: bool = True
    license_type: Optional[str] = None
    version: Optional[str] = None
    platform: Optional[str] = None
    stock: int = 0
    is_promoted: bool = False

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    release_date: date

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    email: str
    name: str
    country: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    created_at: datetime
    is_admin: bool = False
    admin_role: str = "user"
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int = 1
    price_at_purchase: float

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: int
    order_id: int
    product: Product

    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    user_id: int
    status: str = "Pending"
    total_amount: float

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class Order(OrderBase):
    id: int
    created_at: datetime
    items: List[OrderItem]

    class Config:
        from_attributes = True

class SubscriptionBase(BaseModel):
    user_id: int
    product_id: int
    start_date: date
    end_date: date
    auto_renew: bool = True

class SubscriptionCreate(SubscriptionBase):
    pass

class Subscription(SubscriptionBase):
    id: int
    product: Product

    class Config:
        from_attributes = True 