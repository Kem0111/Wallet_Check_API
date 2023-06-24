from pydantic import EmailStr, Field, BaseModel


class Register(BaseModel):
    email: EmailStr
    password: str = Field(..., max_length=30)
