import ormar
from core.db import BaseMeta
from uuid import UUID, uuid4
from passlib.hash import bcrypt
import datetime


class User(ormar.Model):
    class Meta(BaseMeta):
        pass

    id: UUID = ormar.UUID(primary_key=True, default=uuid4)
    last_name: str = ormar.String(max_length=50, nullable=True)
    name: str = ormar.String(max_length=50, nullable=True)
    photo: str = ormar.Text(nullable=True)
    description: str = ormar.Text(nullable=True)
    username: str = ormar.String(max_length=50, unique=True)
    password_hash: str = ormar.String(max_length=128)
    is_organization: bool = ormar.Boolean(nullable=False)
    is_admin: bool = ormar.Boolean(nullable=False)

    @classmethod
    async def get_user(cls, username):
        return cls.get(username=username)

    def verify_password(self, password):
        return bcrypt.verify(password, self.password_hash)


class Course(ormar.Model):
    class Meta(BaseMeta):
        pass

    id: UUID = ormar.UUID(primary_key=True, default=uuid4)
    name: str = ormar.String(max_length=100, nullable=True)
    price: float = ormar.Float(nullable=True)
    organization: str = ormar.String(max_length=50, nullable=True)
    sphere: str = ormar.String(max_length=50, nullable=True)
    language: str = ormar.String(max_length=50, nullable=True)
    description: str = ormar.Text(nullable=True)
    is_certificate: bool = ormar.Boolean(nullable=True)
    link: str = ormar.Text(nullable=True)
    data: datetime.date = datetime.date.today()


class Certificate(ormar.Model):
    class Meta(BaseMeta):
        pass

    id: UUID = ormar.UUID(primary_key=True, default=uuid4)
    user_id: UUID = ormar.UUID(nullable=False)
    name: str = ormar.String(nullable=False, max_length=50)
    link: str = ormar.Text(nullable=True)


class Processe(ormar.Model):
    class Meta(BaseMeta):
        pass

    id: UUID = ormar.UUID(primary_key=True, default=uuid4)
    user_id: UUID = ormar.UUID(nullable=False)
    course_id: UUID = ormar.UUID(nullable=False)


class Passed(ormar.Model):
    class Meta(BaseMeta):
        pass

    id: UUID = ormar.UUID(primary_key=True, default=uuid4)
    user_id: UUID = ormar.UUID(nullable=False)
    course_id: UUID = ormar.UUID(nullable=False)
