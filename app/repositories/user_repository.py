from typing import Optional
from uuid import UUID
from sqlmodel import Session, select
from app.models.user import User


class UserRepository:

    def __init__(self, session: Session):
        self.session = session

    def save(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def find_by_id(self, user_id: UUID) -> Optional[User]:
        statement = select(User).where(User.id == user_id)
        return self.session.exec(statement).first()

    def find_by_email(self, email: str) -> Optional[User]:
        statement = select(User).where(User.email == email)
        return self.session.exec(statement).first()

    def exists_by_email(self, email: str) -> bool:
        return self.find_by_email(email) is not None