from pydantic import EmailStr, Field, BaseModel


class Register(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(..., max_length=30)
