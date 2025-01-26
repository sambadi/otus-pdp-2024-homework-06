import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from homework_06.infrastructure.orm import Base


@pytest.fixture(scope="function", autouse=True)
def db_session(request):
    engine = create_engine("sqlite://", echo=True)
    factory = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    yield factory()
    Base.metadata.drop_all(engine)
