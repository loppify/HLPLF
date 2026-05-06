import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finance_project.settings')
django.setup()

from django.contrib.auth.models import User
from transactions.models import Category, Transaction

def populate_data():
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin')
        print("Суперкористувача створено: логін - admin, пароль - admin")

    if not Category.objects.exists():
        cat_salary = Category.objects.create(name="Зарплата")
        cat_food = Category.objects.create(name="Їжа")
        cat_rent = Category.objects.create(name="Оренда")
        cat_transport = Category.objects.create(name="Транспорт")

        Transaction.objects.create(
            description="Аванс",
            amount=Decimal('15000.00'),
            transaction_type='debit',
            category=cat_salary
        )
        Transaction.objects.create(
            description="Продукти в Сільпо",
            amount=Decimal('1200.50'),
            transaction_type='credit',
            category=cat_food
        )
        Transaction.objects.create(
            description="Квартплата",
            amount=Decimal('4500.00'),
            transaction_type='credit',
            category=cat_rent
        )
        Transaction.objects.create(
            description="Метро та маршрутка",
            amount=Decimal('350.00'),
            transaction_type='credit',
            category=cat_transport
        )
        print("Тестові дані успішно додано!")

if __name__ == '__main__':
    populate_data()
