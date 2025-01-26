from sqlalchemy.orm import Session

from homework_06.domain.unit_of_work import UnitOfWork


class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session: Session):
        self.__session = session

    def __enter__(self):
        self.__session.begin()
        return self

    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()
