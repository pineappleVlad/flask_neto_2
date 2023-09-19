import pydantic
import typing


class CreateAdv(pydantic.BaseModel):
    header: str
    description: str
    owner: str

class UpdateAdv(pydantic.BaseModel):
    header: typing.Optional[str]
    description: typing.Optional[str]
    owner: typing.Optional[str]