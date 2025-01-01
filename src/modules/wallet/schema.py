from pydantic import BaseModel, EmailStr


class Set_Pin_Schema(BaseModel):
    email: EmailStr
    pin: str

    class Config:
        form_attributes = True


class Transfer_Schema(BaseModel):
    amount: int

    class Config:
        form_attributes = True
