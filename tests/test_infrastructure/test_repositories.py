from homework_06.domain.models import Customer, Product, Order
from homework_06.infrastructure.repositories import (
    SqlAlchemyCustomerRepository,
    SqlAlchemyProductRepository,
    SqlAlchemyOrderRepository,
)


def test_repositories(db_session):
    customer_repo = SqlAlchemyCustomerRepository(db_session)
    product_repo = SqlAlchemyProductRepository(db_session)
    order_repo = SqlAlchemyOrderRepository(db_session)

    customer = Customer(
        id=None, name="John Dow", organization="Hampelmann Incorporated"
    )
    customer_repo.add(customer)

    product = Product(id=None, name="Simple thing", quantity=10, price=10)
    product_repo.add(product)

    order = Order(id=None, customer=customer, products=[product])
    order_repo.add(order)

    assert customer.id
    assert customer_repo.get(customer_id=customer.id) == customer
    assert product.id
    assert product_repo.get(product_id=product.id) == product
    assert order.id
    assert order_repo.get(order_id=order.id) == order

    assert customer_repo.list() == [customer]
    assert product_repo.list() == [product]
    assert order_repo.list() == [order]
