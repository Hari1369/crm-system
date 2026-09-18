from pydantic import BaseModel, AnyUrl, Field, EmailStr, field_validator
from typing import List, Dict
import json


class Ticket_User(BaseModel):
    customer_name       : str = Field(max_length = 50)
    customer_email      : EmailStr
    subject             : str
    description         : str


    @field_validator('customer_email')
    @classmethod
    def email_validator(cls, value):
        valid_domains = ["gmail.com"]
        domain_name = str(value).split('@')[-1]

        if domain_name not in valid_domains:
            raise ValueError("Not a Valid domain")
        else:
            return value

    @field_validator('customer_name')
    @classmethod
    def transform_name(cls, value):

        return value.upper()