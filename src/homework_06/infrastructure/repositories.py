from sqlalchemy.orm import Session
from homework_06.domain.models import Customer, Order, Product
from homework_06.domain.repositories import (
    CustomerRepository,
    ProductRepository,
    OrderRepository,
)
from homework_06.infrastructure.orm import CustomerORM, ProductORM, OrderORM


class SqlAlchemyCustomerRepository(CustomerRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, customer: Customer):
        customer_orm = CustomerORM(
            name=customer.name,
            organization=customer.organization,
        )
        self.session.add(customer_orm)
        self.session.flush()
        customer.id = customer_orm.id

    def get(self, customer_id: int) -> Customer:
        customer_orm = self.session.query(CustomerORM).filter_by(id=customer_id).one()
        return Customer(
            id=customer_orm.id,
            name=customer_orm.name,
            organization=customer_orm.organization,
        )

    def list(self) -> list[Customer]:
        customers_orm = self.session.query(CustomerORM).all()
        return [
            Customer(id=c.id, name=c.name, organization=c.organization)
            for c in customers_orm
        ]


class SqlAlchemyProductRepository(ProductRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, product: Product):
        product_orm = ProductORM(
            name=product.name, quantity=product.quantity, price=product.price
        )
        self.session.add(product_orm)
        self.session.flush()
        product.id = product_orm.id

    def get(self, product_id: int) -> Product:
        product_orm = self.session.query(ProductORM).filter_by(id=product_id).one()
        return Product(
            id=product_orm.id,
            name=product_orm.name,
            quantity=product_orm.quantity,
            price=product_orm.price,
        )

    def list(self) -> list[Product]:
        products_orm = self.session.query(ProductORM).all()
        return [
            Product(id=p.id, name=p.name, quantity=p.quantity, price=p.price)
            for p in products_orm
        ]


class SqlAlchemyOrderRepository(OrderRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, order: Order):
        order_orm = OrderORM()
        order_orm.customer = (
            self.session.query(CustomerORM).filter_by(id=order.customer.id).one()
        )
        order_orm.products = [
            self.session.query(ProductORM).filter_by(id=p.id).one()
            for p in order.products
        ]
        self.session.add(order_orm)
        self.session.flush()
        order.id = order_orm.id

    def get(self, order_id: int) -> Order:
        order_orm = self.session.query(OrderORM).filter_by(id=order_id).one()
        customer = Customer(
            id=order_orm.customer.id,
            name=order_orm.customer.name,
            organization=order_orm.customer.organization,
        )
        products = [
            Product(id=p.id, name=p.name, quantity=p.quantity, price=p.price)
            for p in order_orm.products
        ]
        return Order(id=order_orm.id, customer=customer, products=products)

    def list(self) -> list[Order]:
        orders_orm = self.session.query(OrderORM).all()
        orders = []
        for order_orm in orders_orm:
            products = [
                Product(id=p.id, name=p.name, quantity=p.quantity, price=p.price)
                for p in order_orm.products
            ]
            customer = Customer(
                id=order_orm.customer.id,
                name=order_orm.customer.name,
                organization=order_orm.customer.organization,
            )
            orders.append(Order(id=order_orm.id, customer=customer, products=products))
        return orders
