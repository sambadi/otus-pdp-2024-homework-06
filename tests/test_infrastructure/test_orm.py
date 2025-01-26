from homework_06.infrastructure.orm import CustomerORM, ProductORM, OrderORM


def test_orm(db_session):
    customer = CustomerORM(name="John Dow", organization="Test Org.")
    db_session.add(customer)

    product = ProductORM(name="Simple Thing", quantity=10, price=10.3)
    db_session.add(product)

    order = OrderORM(customer=customer, products=[product])
    db_session.add(order)

    db_session.commit()

    assert order.id is not None
    assert product.id is not None
    assert customer.id is not None

    assert order.customer == customer
    assert order.customer_id == customer.id
    assert order.products == [product]
