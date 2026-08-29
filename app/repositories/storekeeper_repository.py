from typing import Optional
from uuid import UUID

from sqlmodel import Session, select

from app.models.store_keeper import StoreKeeper


class StoreKeeperRepository:

    def __init__(self, session: Session):
        self.session = session

    def save(self, storekeeper: StoreKeeper) -> StoreKeeper:
        self.session.add(storekeeper)
        self.session.commit()
        self.session.refresh(storekeeper)
        return storekeeper

    def find_by_id(
        self,
        storekeeper_id: UUID
    ) -> Optional[StoreKeeper]:
        statement = select(StoreKeeper).where(
            StoreKeeper.id == storekeeper_id
        )

        return self.session.exec(statement).first()

    def find_by_email(
        self,
        email: str
    ) -> Optional[StoreKeeper]:
        statement = select(StoreKeeper).where(
            StoreKeeper.email == email
        )

        return self.session.exec(statement).first()

    def exists_by_email(self, email: str) -> bool:
        return self.find_by_email(email) is not None