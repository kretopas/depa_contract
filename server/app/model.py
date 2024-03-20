# app/model.py

from datetime import datetime
from pydantic import BaseModel, Field, constr

class UserLoginSchema(BaseModel):
    username: str = Field(...)
    password: str = Field(...)

class UserRegister():
    def __init__(self, data: dict) -> None:
        self.name = data['name']
        self.company = data['company']
        self.email = data['email']
        self.username = data['username']
        self.password = data['password']

    def __str__(self) -> str:
        user = f"""
        Name: {self.name}
        Company: {self.company}
        Email: {self.email}
        Username: {self.username}
        Password: {self.password}
        """
        return user

class UserEdit():
    def __init__(self, data: dict) -> None:
        self.name = data['name']
        self.company = data['company']
        self.email = data['email']

class OtpBaseSchema(BaseModel):
    username: str
    otp_enable: bool = False
    otp_verified: bool = False
    otp_base32: str | None = None
    created_at: datetime | None = datetime.now()
    updated_at: datetime | None = datetime.now()

class OtpRequestSchema(BaseModel):
    username: str
    password: str | None = None
    token: str | None = None
    
class LogSchema(BaseModel):
    username: str
    action: str
    path: str
    created_at: datetime | None = datetime.now()