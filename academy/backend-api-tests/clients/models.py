"""Контракты ответов API.

extra='forbid': новое или пропавшее поле ломает тест — так ловится
незаметное изменение контракта, о котором фронтенд не знает.
"""
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Contract(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True)


class UserView(Contract):
    id: int
    email: str
    name: str
    role: Literal['customer', 'admin']


class LoginView(Contract):
    token: str = Field(min_length=20)
    user: UserView
    expires_in: int


class ProductView(Contract):
    id: int
    name: str
    category: Literal['accessories', 'screens', 'computers', 'audio']
    price: int = Field(gt=0)
    stock: int = Field(ge=0)
    description: str
    active: bool


class CartItemView(Contract):
    product_id: int
    name: str
    quantity: int = Field(ge=1)
    price: int


class CartView(Contract):
    items: list[CartItemView]
    total: int = Field(ge=0)


class OrderItemView(Contract):
    product_id: int
    quantity: int
    price: int


class OrderView(Contract):
    id: int
    status: Literal['new', 'payment_pending', 'paid', 'cancelled']
    total: int
    address: str
    coupon: str
    items: list[OrderItemView]


class ErrorView(BaseModel):
    detail: str | list
