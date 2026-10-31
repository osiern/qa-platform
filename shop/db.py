from datetime import datetime, timezone
from sqlalchemy import create_engine, ForeignKey, String, Integer, DateTime, JSON, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from shop.settings import DATABASE_URL


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(100), default='Студент')
    role: Mapped[str] = mapped_column(String(20), default='customer')


class Product(Base):
    __tablename__ = 'products'
    __table_args__ = (CheckConstraint('price > 0'), CheckConstraint('stock >= 0'))
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150))
    category: Mapped[str] = mapped_column(String(30))
    price: Mapped[int] = mapped_column(Integer)  # копейки, без float
    stock: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(String(500), default='Учебный товар')
    active: Mapped[bool] = mapped_column(default=True)


class Order(Base):
    __tablename__ = 'orders'
    __table_args__ = (UniqueConstraint('user_id', 'idem'), CheckConstraint('total >= 0'))
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    idem: Mapped[str] = mapped_column(String(100))
    fingerprint: Mapped[str] = mapped_column(String(64))
    status: Mapped[str] = mapped_column(String(30), default='new')
    total: Mapped[int] = mapped_column(Integer)
    address: Mapped[str] = mapped_column(String(300))
    coupon: Mapped[str] = mapped_column(String(30), default='')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class OrderItem(Base):
    __tablename__ = 'order_items'
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id', ondelete='CASCADE'))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    quantity: Mapped[int] = mapped_column(Integer)
    price: Mapped[int] = mapped_column(Integer)
    __table_args__ = (CheckConstraint('quantity > 0'),)


class Outbox(Base):
    __tablename__ = 'outbox'
    event_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id', ondelete='CASCADE'), unique=True)
    payload: Mapped[dict] = mapped_column(JSON)
    published: Mapped[bool] = mapped_column(default=False)


class PaymentEvent(Base):
    __tablename__ = 'payment_events'
    event_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id', ondelete='CASCADE'), unique=True)
    amount: Mapped[int] = mapped_column(Integer)


engine = create_engine(DATABASE_URL, pool_pre_ping=True)
Session = sessionmaker(engine, expire_on_commit=False)
