from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import date
from enum import Enum
from typing import Optional

class GenderEnum(str, Enum):
    male = "Male"
    female = "Female"
    other = "Other"

class AccountTypeEnum(str, Enum):
    savings = "Savings"
    current = "Current"
    student = "Student"

class EmploymentStatusEnum(str, Enum):
    employed = "Employed"
    self_employed = "Self-Employed"
    student = "Student"
    unemployed = "Unemployed"
    retired = "Retired"

# Nested Address Model
class Address(BaseModel):
    street: str
    city: str
    state: str
    pincode: str = Field(..., pattern=r'^\d{6}$')

class UserData(BaseModel):
    """Schema for user registration data."""
    
    fullname: str
    parentname: str
    dob: date
    gender: GenderEnum
    phone: str = Field(..., pattern=r'^\d{10}$')
    email: EmailStr
    address: Address  # Using the nested Address model
    accountType: AccountTypeEnum
    employment: EmploymentStatusEnum
    deposit: int
    nominee: str
    toggle_2fa: bool = False
    toggle_allowTransactions: bool = False
    toggle_alerts: bool = False
    toggle_newsletters: bool = False
    
    @field_validator('dob')
    def validate_age(cls, v: date):
        """Ensure user is at least 18 years old."""
        today = date.today()
        age = today.year - v.year - ((today.month, today.day) < (v.month, v.day))
        if age < 18:
            raise ValueError("User must be at least 18 years old.")
        return v

    @field_validator('toggle_2fa', 'toggle_allowTransactions', 'toggle_alerts', 'toggle_newsletters', mode='before')
    def convert_toggle_to_bool(cls, value):
        """Convert 'on'/'off' strings to boolean values."""
        if isinstance(value, str):
            return value.lower() == 'on'
        return bool(value)

    @field_validator('deposit', mode='before')
    def convert_deposit_to_int(cls, value):
        """Ensure deposit is integer."""
        return int(value)
