from typing import Optional
from uuid import UUID

from sqlmodel import Session, select

from app.models.customer import Customer


class CustomerRepository:

    def __init__(self, session: Session):
        self.session = session

    def save(self, customer: Customer) -> Customer:
        self.session.add(customer)
        self.session.commit()
        self.session.refresh(customer)
        return customer

    def find_by_id(self, customer_id: UUID) -> Optional[Customer]:
        statement = select(Customer).where(Customer.id == customer_id)
        return self.session.exec(statement).first()

    def find_by_email(self, email: str) -> Optional[Customer]:
        statement = select(Customer).where(Customer.email == email)
        return self.session.exec(statement).first()

    def exists_by_email(self, email: str) -> bool:
        return self.find_by_email(email) is not None