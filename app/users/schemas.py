from pydantic import BaseModel, EmailStr, ConfigDict


class SUserAuth(BaseModel):
    password: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)
