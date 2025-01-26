import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from homework_06.domain.services import WarehouseService, CustomerService
from homework_06.infrastructure.orm import Base
from homework_06.infrastructure.repositories import (
    SqlAlchemyProductRepository,
    SqlAlchemyOrderRepository,
    SqlAlchemyCustomerRepository,
)
from homework_06.infrastructure.unit_of_work import SqlAlchemyUnitOfWork
from homework_06.infrastructure.database import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionFactory = sessionmaker(bind=engine)
logger = logging.getLogger()
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
)


def main():
    logger.info("Init repos")
    session = SessionFactory()
    customer_repo = SqlAlchemyCustomerRepository(session)
    product_repo = SqlAlchemyProductRepository(session)
    order_repo = SqlAlchemyOrderRepository(session)
    logger.info("Init Unit of Work")
    uow = SqlAlchemyUnitOfWork(session)
    customer_service = CustomerService(customer_repo)
    warehouse_service = WarehouseService(product_repo, order_repo)

    with uow:
        logger.info("Start UoW")
        new_customer = customer_service.create_customer(
            name="John Dow", organization="Simple Works"
        )
        logger.info(f"New customer: {new_customer} created")
        new_product = warehouse_service.create_product(
            name="test1", quantity=1, price=100
        )
        logger.info(f"New product: {new_product} created")
        new_order = warehouse_service.create_order(
            customer=new_customer, products=[new_product]
        )
        logger.info(f"New order: {new_order} created")
        uow.commit()
        logger.info("Committed all work")

    with uow:
        logger.info("Start UoW")
        logger.info(f"List all orders: {order_repo.list()} in new unit of work")


if __name__ == "__main__":
    logger.info("Start demo")
    try:
        logger.info("Create database objects")
        Base.metadata.create_all(engine)

        main()
    finally:
        logger.info("Stop demo and rollback database state to zero point")
        Base.metadata.drop_all(engine)
