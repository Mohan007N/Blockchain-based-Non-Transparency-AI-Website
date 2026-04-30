"""
Loan Verification models
"""
from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime
from beanie import Document


class FileAttachment(BaseModel):
    """File attachment metadata"""
    original_name: str
    stored_name: str
    path: str
    mimetype: str
    size: int
    document_type: str
    url: str
    uploaded_at: datetime = datetime.utcnow()


class ExtractedData(BaseModel):
    """Extracted data from documents"""
    raw_text: Optional[str] = None
    extraction_confidence: Optional[float] = None
    applicant_name: Optional[str] = None
    pan_number: Optional[str] = None
    aadhaar_number: Optional[str] = None
    monthly_income: Optional[float] = None
    annual_income: Optional[float] = None
    employer_name: Optional[str] = None
    employment_type: Optional[str] = None
    account_number: Optional[str] = None
    bank_name: Optional[str] = None
    average_balance: Optional[float] = None
    credit_score: Optional[int] = None
    existing_loans: Optional[int] = None
    property_value: Optional[float] = None
    loan_amount_requested: Optional[float] = None


class RuleCheck(BaseModel):
    """Individual rule check result"""
    rule: str
    passed: bool
    message: str
    is_mandatory: bool = False


class AiDecision(BaseModel):
    """AI decision result"""
    recommendation: str  # approve, reject, manual_review
    score: float
    rule_checks: List[RuleCheck] = []
    mandatory_passed: int = 0
    mandatory_total: int = 0
    summary: str
    processed_at: datetime = datetime.utcnow()


class ManagerAction(BaseModel):
    """Manager action on verification"""
    manager_id: str
    manager_name: str
    action: str  # approved, rejected, requested_info
    comments: Optional[str] = None
    timestamp: datetime = datetime.utcnow()


class LoanVerification(Document):
    """Loan verification document"""
    user_id: str
    application_id: str
    files: List[FileAttachment] = []
    loan_type: str = "personal"
    status: str = "pending"  # pending, processing, ai_reviewed, approved, rejected
    result: Optional[str] = None  # Approved, Rejected, Under Review
    reason: Optional[str] = None
    
    extracted_data: Optional[ExtractedData] = None
    ai_decision: Optional[AiDecision] = None
    
    manager_actions: List[ManagerAction] = []
    processing_errors: List[str] = []
    
    ocr_provider: Optional[str] = None
    processing_time_ms: Optional[int] = None
    
    ip_address: Optional[str] = None
    
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
    
    class Settings:
        name = "loan_verifications"
        use_state_management = True
