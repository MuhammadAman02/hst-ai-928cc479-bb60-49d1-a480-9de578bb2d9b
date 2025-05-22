"""
Transaction data models.
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
import uuid


class TransactionType(str, Enum):
    """Transaction types."""
    CARD_PAYMENT = "card_payment"
    CARD_WITHDRAWAL = "card_withdrawal"
    BANK_TRANSFER = "bank_transfer"
    DIRECT_DEBIT = "direct_debit"
    STANDING_ORDER = "standing_order"
    MOBILE_PAYMENT = "mobile_payment"
    ONLINE_PAYMENT = "online_payment"
    OTHER = "other"


class TransactionStatus(str, Enum):
    """Transaction status."""
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REVERSED = "reversed"
    FLAGGED = "flagged"
    BLOCKED = "blocked"


class FraudRiskLevel(str, Enum):
    """Fraud risk levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    UNKNOWN = "unknown"


class Location(BaseModel):
    """Location data model."""
    country: str
    city: Optional[str] = None
    postal_code: Optional[str] = None
    ip_address: Optional[str] = None
    coordinates: Optional[Dict[str, float]] = None


class Transaction(BaseModel):
    """Transaction data model."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    account_id: str
    amount: float
    currency: str = "EUR"
    description: Optional[str] = None
    transaction_type: TransactionType
    merchant_name: Optional[str] = None
    merchant_category: Optional[str] = None
    status: TransactionStatus = TransactionStatus.COMPLETED
    location: Optional[Location] = None
    device_info: Optional[Dict[str, Any]] = None
    
    @validator('amount')
    def amount_must_be_positive(cls, v):
        """Validate that amount is positive."""
        if v <= 0:
            raise ValueError('Amount must be positive')
        return v


class TransactionWithRisk(Transaction):
    """Transaction with fraud risk assessment."""
    risk_score: float = 0.0
    risk_level: FraudRiskLevel = FraudRiskLevel.UNKNOWN
    risk_factors: List[str] = []
    is_fraudulent: Optional[bool] = None
    reviewed_by: Optional[str] = None
    review_notes: Optional[str] = None
    review_timestamp: Optional[datetime] = None


class FraudCase(BaseModel):
    """Fraud case data model."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    account_id: str
    transactions: List[str]  # List of transaction IDs
    risk_level: FraudRiskLevel
    status: str = "open"  # open, investigating, closed, false_positive
    assigned_to: Optional[str] = None
    resolution: Optional[str] = None
    notes: Optional[str] = None