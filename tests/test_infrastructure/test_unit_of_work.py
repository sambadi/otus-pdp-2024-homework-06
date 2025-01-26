import pytest
from sqlalchemy.exc import NoResultFound

from homework_06.domain.models import Customer
from homework_06.domain.services import CustomerService
from homework_06.infrastructure.repositories import SqlAlchemyCustomerRepository
from homework_06.infrastructure.unit_of_work import SqlAlchemyUnitOfWork


def test_unit_of_work(db_session):
    customer_repo = SqlAlchemyCustomerRepository(db_session)

    uow = SqlAlchemyUnitOfWork(db_session)
    customer_service = CustomerService(customer_repo)

    with uow:
        assert not customer_repo.list()

    customer: Customer | None

    with uow:
        customer = customer_service.create_customer(
            name="John Dow", organization="Hampelmann Incorporated"
        )
        assert customer.id
        assert customer_repo.get(customer_id=customer.id) == customer
        uow.rollback()

    assert customer

    with uow:
        with pytest.raises(NoResultFound):
            _ = customer_repo.get(customer_id=customer.id)
        assert not customer_repo.list()

    with uow:
        customer = customer_service.create_customer(
            name="John Dow", organization="Hampelmann Incorporated"
        )
        uow.commit()

    assert customer
    assert customer.id

    with uow:
        assert customer_repo.list() == [customer]
