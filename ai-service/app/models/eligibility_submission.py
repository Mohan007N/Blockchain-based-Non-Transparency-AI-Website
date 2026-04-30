"""
Eligibility Submission models
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from beanie import Document


class GteProofPublicInputs(BaseModel):
    """Greater-than-or-equal proof public inputs"""
    threshold: int
    commitment: str  # commitment to the actual value


class ProofPacket(BaseModel):
    """ZKP proof packet"""
    proof_type: str  # income, credit_score, employment
    proof_data: str  # encrypted/hashed proof
    verification_hash: str
    public_inputs: Optional[GteProofPublicInputs] = None
    timestamp: datetime = datetime.utcnow()


class EligibilitySubmission(Document):
    """Eligibility submission document"""
    user_id: str
    loan_type: str
    loan_amount: float
    
    # ZKP proofs
    income_proof: Optional[ProofPacket] = None
    credit_score_proof: Optional[ProofPacket] = None
    employment_proof: Optional[ProofPacket] = None
    
    # Results
    is_eligible: Optional[bool] = None
    eligibility_score: Optional[float] = None
    reasons: List[str] = []
    
    status: str = "pending"  # pending, verified, approved, rejected
    
    submitted_at: datetime = datetime.utcnow()
    processed_at: Optional[datetime] = None
    
    class Settings:
        name = "eligibility_submissions"
        use_state_management = True
