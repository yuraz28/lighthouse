from uuid import UUID
from pydantic import BaseModel
import orjson
from typing import Optional


class BaseSchema(BaseModel):
    class Config:
        anystr_strip_whitespace = True
        min_anystr_length = 1
        json_loads = orjson.loads
        json_dumps = orjson.dumps


class UserAllInfo(BaseSchema):
    last_name: Optional[str]
    name: str
    username: str
    password_hash: str
    is_organization: bool = False
    is_admin: bool


class OrgAllInfo(BaseSchema):
    username: str
    name: str
    password_hash: str
    is_organization: bool = True
    is_admin: bool = False


class UserAuth(BaseSchema):
    username: str
    password_hash: str


class UserGet(BaseSchema):
    id: str
    username: str
    password_hash: str


class UserEdit(BaseSchema):
    last_name: Optional[str]
    name: Optional[str]
    photo: Optional[str]
    description: Optional[str]
    username: Optional[str]
    password_hash: Optional[str]


class CheckEmail(BaseSchema):
    username: str


class CheckAnswer(BaseSchema):
    answer: bool


class CreateCourse(BaseSchema):
    name: str
    price: float
    organization: Optional[str]
    sphere: str
    language: str
    description: str
    is_certificate: bool
    link: str


class CertificateAllInfo(BaseSchema):
    user_id: UUID
    name: str
    link: str


class AddMyCourse(BaseSchema):
    user_id: UUID
    course_id: UUID


