from homework_06.domain.models import Customer, Product, Order, BaseModel
from homework_06.domain.repositories import (
    CustomerRepository,
    ProductRepository,
    OrderRepository,
)


class InMemoryStorage[T: BaseModel]:
    def __init__(self):
        self.idx: int = 1
        self._storage: dict[int, T] = {}

    def add(self, item: T):
        if item.id is None:
            item.id = self.idx
            self.idx += 1

        self._storage[item.id] = item

    def get(self, item_id: int) -> T:
        return self._storage[item_id]

    def list(self) -> list[T]:
        return list(self._storage.values())


class InMemoryCustomerRepository(CustomerRepository):
    def __init__(self):
        self._storage: InMemoryStorage[Customer] = InMemoryStorage[Customer]()

    def add(self, customer: Customer):
        self._storage.add(customer)

    def get(self, customer_id: int) -> Customer:
        return self._storage.get(customer_id)

    def list(self) -> list[Customer]:
        return self._storage.list()


class InMemoryProductRepository(ProductRepository):
    def __init__(self):
        self._storage: InMemoryStorage[Product] = InMemoryStorage[Product]()

    def add(self, product: Product):
        self._storage.add(product)

    def get(self, product_id: int) -> Product:
        return self._storage.get(product_id)

    def list(self) -> list[Product]:
        return self._storage.list()


class InMemoryOrderRepository(OrderRepository):
    def __init__(self):
        self._storage: InMemoryStorage[Order] = InMemoryStorage[Order]()

    def add(self, order: Order):
        self._storage.add(order)

    def get(self, order_id: int) -> Order:
        return self._storage.get(order_id)

    def list(self) -> list[Order]:
        return self._storage.list()
