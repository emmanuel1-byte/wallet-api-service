from pydantic import BaseModel, EmailStr, Field, field_validator


class Signup_Schema(BaseModel):
    fullname: str
    email: EmailStr
    password: str = Field(min_length=8, max_length=256)
    phone: str

    class Config:
        form_attributes = True


class Login_Schema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=256)

    class Config:
        form_attributes = True


class Email_Schema(BaseModel):
    email: EmailStr

    class Config:
        form_attributes = True


class Reset_Password_Schema(BaseModel):
    token: str
    password: str
    confirm_password: str

    @field_validator("confirm_password", mode="before")
    @classmethod
    def password_match(cls, v, values):
        if "password" in values.data and values.data["password"] != v:
            raise ValueError("Password do not match")

        return v

    class Config:
        form_attributes = True
