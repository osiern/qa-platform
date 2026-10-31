from sqlalchemy import select, text
from shop.db import Base, engine, Session, Product, User
from shop.security import hash_password
from shop.settings import ADMIN_EMAIL, ADMIN_PASSWORD


def main():
    # Схема v1. Для обучения миграциям следующую версию переносим на Alembic.
    Base.metadata.create_all(engine)
    with Session.begin() as db:
        db.execute(text('SELECT pg_advisory_xact_lock(817230)'))
        if not db.scalar(select(User).where(User.email == ADMIN_EMAIL)):
            db.add(User(email=ADMIN_EMAIL, password_hash=hash_password(ADMIN_PASSWORD), name='Администратор', role='admin'))
        # Витрина из 15 товаров. Добавляем только отсутствующие по названию,
        # поэтому повторный запуск ничего не дублирует, а в уже созданную БД
        # новые товары доезжают без пересоздания тома.
        for name, category, price, stock, description in [
            ('Клавиатура', 'accessories', 300000, 10000, 'Учебный товар'),
            ('Мышь', 'accessories', 150000, 10000, 'Учебный товар'),
            ('Монитор', 'screens', 2000000, 10000, 'Учебный товар'),
            ('Ноутбук', 'computers', 8000000, 10000, 'Учебный товар'),
            ('Кабель', 'accessories', 50000, 10000, 'Учебный товар'),
            ('Наушники', 'audio', 500000, 0, 'Учебный товар'),
            ('Смартфон', 'computers', 3500000, 120, 'Учебный смартфон с большим экраном'),
            ('Планшет', 'computers', 2200000, 45, 'Учебный планшет для работы и чтения'),
            ('Смарт-часы', 'accessories', 1200000, 80, 'Учебные часы с датчиком пульса'),
            ('Веб-камера', 'accessories', 450000, 200, 'Учебная веб-камера Full HD'),
            ('Колонка', 'audio', 600000, 60, 'Учебная беспроводная колонка'),
            ('Микрофон', 'audio', 900000, 25, 'Учебный студийный микрофон'),
            ('Флешка', 'accessories', 80000, 500, 'Учебный USB-накопитель на 32 ГБ'),
            ('Роутер', 'computers', 350000, 70, 'Учебный Wi-Fi роутер'),
            ('Геймпад', 'accessories', 400000, 90, 'Учебный беспроводной геймпад'),
        ]:
            if not db.scalar(select(Product.id).where(Product.name == name)):
                db.add(Product(name=name, category=category, price=price, stock=stock, description=description))


if __name__ == '__main__':
    main()
