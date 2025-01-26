from sqlalchemy import Column, Integer, String, Float, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

order_product_assocoations = Table(
    "order_product_assocoations",
    Base.metadata,
    Column("order_id", ForeignKey("orders.id")),
    Column("product_id", ForeignKey("products.id")),
)


class CustomerORM(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    organization = Column(String)


class ProductORM(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    quantity = Column(Integer)
    price = Column(Float)


class OrderORM(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    customer: "CustomerORM" = relationship(
        "CustomerORM", cascade="all,delete-orphan", lazy="dynamic"
    )
    products: list["ProductORM"] = relationship(
        "ProductORM", secondary=order_product_assocoations
    )
