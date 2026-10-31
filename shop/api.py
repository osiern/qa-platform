import hashlib
import json
import secrets
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Annotated
from fastapi import FastAPI, Depends, Header, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, StrictInt, field_validator
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError
from shop.db import Session, User, Product, Order, OrderItem, Outbox
from shop.security import cache, hash_password, verify_password, session_user
from shop.settings import SESSION_TTL


def fail(status, message):
    raise HTTPException(status, message)


def current_user(authorization: Annotated[str | None, Header()] = None):
    if not authorization or not authorization.startswith('Bearer '):
        fail(401, 'Требуется вход')
    uid = session_user(authorization[7:])
    with Session() as db:
        user = db.get(User, uid) if uid else None
        if not user:
            fail(401, 'Сессия недействительна')
        return user


def admin(user=Depends(current_user)):
    if user.role != 'admin':
        fail(403, 'Требуются права администратора')
    return user


def user_view(user):
    return dict(id=user.id, email=user.email, name=user.name, role=user.role)


def product_view(p):
    return {k: getattr(p, k) for k in ('id', 'name', 'category', 'price', 'stock', 'description', 'active')}


def order_view(db, order):
    items = db.scalars(select(OrderItem).where(OrderItem.order_id == order.id)).all()
    return dict(id=order.id, status=order.status, total=order.total, address=order.address,
        coupon=order.coupon, items=[dict(product_id=i.product_id, quantity=i.quantity, price=i.price) for i in items])


def owned_order(db, oid, uid, lock=False):
    query = select(Order).where(Order.id == oid, Order.user_id == uid)
    row = db.scalar(query.with_for_update() if lock else query)
    if not row:
        fail(404, 'Заказ не найден')
    return row


class Credentials(BaseModel):
    email: str = Field(max_length=255)
    password: str = Field(min_length=8, max_length=128)

    @field_validator('email')
    @classmethod
    def email_valid(cls, value):
        value = value.strip().lower()
        if value.count('@') != 1 or '.' not in value.split('@')[1] or ' ' in value or not value.split('@')[0]:
            raise ValueError('Некорректный email')
        return value


class Profile(BaseModel):
    name: str = Field(min_length=1, max_length=100)

    @field_validator('name')
    @classmethod
    def name_valid(cls, value):
        if not value.strip():
            raise ValueError('Пустое имя')
        return value.strip()


class CartItem(BaseModel):
    product_id: StrictInt = Field(gt=0)
    quantity: StrictInt = Field(ge=1, le=99)


class Checkout(BaseModel):
    address: str = Field(min_length=5, max_length=300)
    coupon: str = Field(default='', max_length=30)

    @field_validator('address')
    @classmethod
    def address_valid(cls, value):
        if len(value.strip()) < 5:
            raise ValueError('Адрес слишком короткий')
        return value.strip()


class ProductInput(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    category: str = Field(pattern='^(accessories|screens|computers|audio)$')
    price: StrictInt = Field(gt=0)
    stock: StrictInt = Field(ge=0)
    description: str = Field(default='Учебный товар', max_length=500)


app = FastAPI(title='QA Market', version='1.0.0')
static = Path(__file__).parent / 'static'
app.mount('/static', StaticFiles(directory=static), name='static')


@app.get('/', include_in_schema=False)
def index():
    return FileResponse(static / 'index.html')


@app.get('/health')
def health():
    with Session() as db:
        db.execute(text('SELECT 1'))
    cache.ping()
    return {'status': 'ok'}


@app.post('/api/users', status_code=201)
def register(body: Credentials):
    try:
        with Session.begin() as db:
            user = User(email=body.email, password_hash=hash_password(body.password))
            db.add(user)
            db.flush()
            result = user_view(user)
        return result
    except IntegrityError:
        fail(409, 'Email уже зарегистрирован')


@app.post('/api/login')
def login(body: Credentials):
    with Session() as db:
        user = db.scalar(select(User).where(User.email == body.email))
        if not user or not verify_password(body.password, user.password_hash):
            fail(401, 'Неверный email или пароль')
        token = secrets.token_urlsafe(32)
        cache.setex('session:' + token, SESSION_TTL, str(user.id))
        return dict(token=token, user=user_view(user), expires_in=SESSION_TTL)


@app.post('/api/logout', status_code=204)
def logout(user=Depends(current_user), authorization: str = Header()):
    cache.delete('session:' + authorization[7:])


@app.get('/api/me')
def me(user=Depends(current_user)):
    return user_view(user)


@app.patch('/api/me')
def profile(body: Profile, user=Depends(current_user)):
    with Session.begin() as db:
        stored = db.get(User, user.id)
        stored.name = body.name
        return user_view(stored)


@app.get('/api/products')
def products(q: str = '', category: str = '', sort: str = Query('id', pattern='^(id|price_asc|price_desc)$'),
             offset: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=100)):
    with Session() as db:
        query = select(Product).where(Product.active.is_(True))
        if q:
            query = query.where(Product.name.ilike('%' + q + '%'))
        if category:
            query = query.where(Product.category == category)
        ordering = {'id': Product.id, 'price_asc': Product.price.asc(), 'price_desc': Product.price.desc()}[sort]
        return [product_view(p) for p in db.scalars(query.order_by(ordering, Product.id).offset(offset).limit(limit))]


@app.get('/api/products/{pid}')
def product(pid: int):
    with Session() as db:
        p = db.get(Product, pid)
        if not p or not p.active:
            fail(404, 'Товар не найден')
        return product_view(p)


@app.post('/api/admin/products', status_code=201)
def create_product(body: ProductInput, user=Depends(admin)):
    with Session.begin() as db:
        p = Product(**body.model_dump())
        db.add(p)
        db.flush()
        return product_view(p)


def cart_key(uid):
    return f'cart:{uid}'


@app.get('/api/cart')
def cart(user=Depends(current_user)):
    values = cache.hgetall(cart_key(user.id))
    with Session() as db:
        items = []
        for pid, quantity in sorted(values.items(), key=lambda pair: int(pair[0])):
            p = db.get(Product, int(pid))
            if p and p.active:
                items.append(dict(product_id=p.id, name=p.name, quantity=int(quantity), price=p.price))
    return dict(items=items, total=sum(i['price'] * i['quantity'] for i in items))


@app.put('/api/cart')
def put_cart(body: CartItem, user=Depends(current_user)):
    with Session() as db:
        p = db.get(Product, body.product_id)
        if not p or not p.active:
            fail(404, 'Товар не найден')
        if p.stock < body.quantity:
            fail(409, 'Недостаточно товара')
    cache.hset(cart_key(user.id), str(body.product_id), str(body.quantity))
    cache.expire(cart_key(user.id), 86400)
    return cart(user)


@app.delete('/api/cart/{pid}', status_code=204)
def delete_cart(pid: int, user=Depends(current_user)):
    cache.hdel(cart_key(user.id), str(pid))


@app.get('/api/favorites')
def favorites(user=Depends(current_user)):
    return sorted(int(v) for v in cache.smembers(f'favorites:{user.id}'))


@app.put('/api/favorites/{pid}', status_code=204)
def favorite(pid: int, user=Depends(current_user)):
    product(pid)
    cache.sadd(f'favorites:{user.id}', pid)


@app.delete('/api/favorites/{pid}', status_code=204)
def unfavorite(pid: int, user=Depends(current_user)):
    cache.srem(f'favorites:{user.id}', pid)


@app.get('/api/orders')
def orders(user=Depends(current_user)):
    with Session() as db:
        return [order_view(db, o) for o in db.scalars(select(Order).where(Order.user_id == user.id).order_by(Order.id.desc()))]


@app.post('/api/orders', status_code=201)
def checkout(body: Checkout, idempotency_key: Annotated[str, Header(min_length=1, max_length=100)], user=Depends(current_user)):
    # Пользователь блокируется до чтения идемпотентности: два одновременных
    # одинаковых запроса не создадут два заказа и не спишут остаток дважды.
    with Session.begin() as db:
        db.scalar(select(User).where(User.id == user.id).with_for_update())
        previous = db.scalar(select(Order).where(Order.user_id == user.id, Order.idem == idempotency_key))
        if previous:
            if previous.address != body.address or previous.coupon != body.coupon:
                fail(409, 'Ключ уже использован с другими параметрами')
            return order_view(db, previous)
        if body.coupon not in ('', 'SAVE10'):
            fail(400, 'Промокод недействителен')
        raw = cache.hgetall(cart_key(user.id))
        if not raw:
            fail(400, 'Корзина пуста')
        entries = []
        for pid in sorted(int(p) for p in raw):
            p = db.scalar(select(Product).where(Product.id == pid).with_for_update())
            qty = int(raw[str(pid)])
            if not p or not p.active or p.stock < qty:
                fail(409, 'Недостаточно товара')
            entries.append((p, qty))
        subtotal = sum(p.price * qty for p, qty in entries)
        total = subtotal * 90 // 100 if body.coupon else subtotal
        fingerprint = hashlib.sha256(json.dumps(raw, sort_keys=True).encode()).hexdigest()
        order = Order(user_id=user.id, idem=idempotency_key, fingerprint=fingerprint,
                      total=total, address=body.address, coupon=body.coupon)
        db.add(order)
        db.flush()
        for p, qty in entries:
            p.stock -= qty
            db.add(OrderItem(order_id=order.id, product_id=p.id, quantity=qty, price=p.price))
        db.flush()
        result = order_view(db, order)
    # PostgreSQL и Redis не образуют общую транзакцию. Повтор запроса безопасен
    # по ключу; редкая ошибка очистки корзины описана как учебное ограничение.
    cache.delete(cart_key(user.id))
    return result


@app.get('/api/orders/{oid}')
def get_order(oid: int, user=Depends(current_user)):
    with Session() as db:
        return order_view(db, owned_order(db, oid, user.id))


@app.post('/api/orders/{oid}/cancel')
def cancel(oid: int, user=Depends(current_user)):
    with Session.begin() as db:
        order = owned_order(db, oid, user.id, lock=True)
        if order.status == 'cancelled':
            return order_view(db, order)
        if order.status != 'new':
            fail(409, 'Заказ уже передан на оплату')
        items = db.scalars(select(OrderItem).where(OrderItem.order_id == oid).order_by(OrderItem.product_id)).all()
        for item in items:
            p = db.scalar(select(Product).where(Product.id == item.product_id).with_for_update())
            p.stock += item.quantity
        order.status = 'cancelled'
        return order_view(db, order)


@app.post('/api/orders/{oid}/pay', status_code=202)
def pay(oid: int, user=Depends(current_user)):
    with Session.begin() as db:
        order = owned_order(db, oid, user.id, lock=True)
        if order.status == 'cancelled':
            fail(409, 'Заказ отменён')
        if order.status == 'new':
            order.status = 'payment_pending'
            event_id = secrets.token_hex(16)
            db.add(Outbox(event_id=event_id, order_id=oid,
                payload=dict(event_id=event_id, order_id=oid, amount=order.total)))
        return dict(id=oid, status=order.status)
