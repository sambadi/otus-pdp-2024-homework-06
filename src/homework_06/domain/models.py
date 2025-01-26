from dataclasses import dataclass, field
from typing import List


@dataclass
class BaseModel:
    id: int | None


@dataclass
class Customer(BaseModel):
    name: str
    organization: str


@dataclass
class Product(BaseModel):
    name: str
    quantity: int
    price: float


@dataclass
class Order(BaseModel):
    customer: Customer
    products: List[Product] = field(default_factory=list)

    def add_product(self, product: Product):
        self.products.append(product)
