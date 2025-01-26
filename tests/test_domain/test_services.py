from homework_06.domain.services import CustomerService, WarehouseService
from tests.test_domain.fake_storages import (
    InMemoryCustomerRepository,
    InMemoryProductRepository,
    InMemoryOrderRepository,
)


def test_services():
    customer_repo = InMemoryCustomerRepository()
    product_repo = InMemoryProductRepository()
    order_repo = InMemoryOrderRepository()

    customer_service = CustomerService(customer_repo)
    customer = customer_service.create_customer(
        name="Jpohn Dow", organization="Hampelmann Incorporated"
    )
    assert customer
    assert customer.id == (customer_repo._storage.idx - 1)

    warehouse_service = WarehouseService(product_repo, order_repo)

    product = warehouse_service.create_product(name="test1", quantity=1, price=100)
    assert product
    assert product.id == (product_repo._storage.idx - 1)

    order = warehouse_service.create_order(customer=customer, products=[product])
    assert order
    assert order.id == (order_repo._storage.idx - 1)
    assert order.customer == customer
    assert len(order.products) == 1
    assert order.products[0] == product
