from homework_06.domain.models import Product, Order, Customer
from .repositories import ProductRepository, OrderRepository, CustomerRepository


class CustomerService:
    def __init__(self, customer_repo: CustomerRepository):
        self.customer_repo = customer_repo

    def create_customer(self, name: str, organization: str) -> Customer:
        customer = Customer(id=None, name=name, organization=organization)
        self.customer_repo.add(customer)
        return customer


class WarehouseService:
    def __init__(self, product_repo: ProductRepository, order_repo: OrderRepository):
        self.product_repo = product_repo
        self.order_repo = order_repo

    def create_product(self, name: str, quantity: int, price: float) -> Product:
        product = Product(id=None, name=name, quantity=quantity, price=price)
        self.product_repo.add(product)
        return product

    def create_order(self, customer: Customer, products: list[Product]) -> Order:
        order = Order(id=None, customer=customer, products=products)
        self.order_repo.add(order)
        return order
