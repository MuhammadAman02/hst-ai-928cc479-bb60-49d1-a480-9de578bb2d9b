"""
Account data models.
"""
from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid


class Account(BaseModel):
    """Account data model."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    account_number: str
    sort_code: str
    account_type: str  # personal, business, etc.
    customer_id: str
    balance: float = 0.0
    currency: str = "EUR"
    status: str = "active"  # active, suspended, closed
    risk_profile: Optional[Dict[str, Any]] = None
    
    @validator('sort_code')
    def validate_sort_code(cls, v):
        """Validate Irish sort code format."""
        # Irish sort codes are typically 6 digits, often written as 3 pairs
        v = v.replace("-", "")
        if not (v.isdigit() and len(v) == 6):
            raise ValueError('Sort code must be 6 digits')
        return v
    
    @validator('account_number')
    def validate_account_number(cls, v):
        """Validate Irish account number format."""
        # Irish account numbers are typically 8 digits
        v = v.replace(" ", "")
        if not (v.isdigit() and len(v) == 8):
            raise ValueError('Account number must be 8 digits')
        return v


class Customer(BaseModel):
    """Customer data model."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[Dict[str, str]] = None
    date_of_birth: Optional[datetime] = None
    pps_number: Optional[str] = None  # Irish Personal Public Service Number
    accounts: List[str] = []  # List of account IDs
    risk_score: float = 0.0
    
    @validator('pps_number')
    def validate_pps_number(cls, v):
        """Validate Irish PPS number format if provided."""
        if v is None:
            return v
            
        # PPS numbers are 7 digits followed by 1 or 2 letters
        v = v.upper().replace(" ", "")
        if not (len(v) in [8, 9] and v[0:7].isdigit() and v[7:].isalpha()):
            raise ValueError('Invalid PPS number format')
        return v