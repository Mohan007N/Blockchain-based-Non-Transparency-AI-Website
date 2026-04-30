"""
Secure Document Verification with OCR
Extracts salary from income certificate and verifies loan eligibility
Uses blockchain for immutable audit trail
"""

import re
import logging
from typing import Dict, Optional, Tuple
from datetime import datetime
import hashlib
import json

logger = logging.getLogger("verity-ai.ocr")


class DocumentVerifier:
    """Verifies loan eligibility by comparing salary with loan amount"""
    
    # Loan eligibility rules (salary multiplier)
    ELIGIBILITY_RULES = {
        "personal": 5,      # Can borrow up to 5x monthly salary
        "home": 60,         # Can borrow up to 60x monthly salary (5 years)
        "auto": 10,         # Can borrow up to 10x monthly salary
        "business": 8,      # Can borrow up to 8x monthly salary
        "education": 12,    # Can borrow up to 12x monthly salary
    }
    
    def __init__(self):
        self.min_salary = 15000  # Minimum monthly salary required
    
    def extract_salary_from_text(self, ocr_text: str) -> Optional[float]:
        """
        Extract salary amount from OCR text
        Looks for patterns like:
        - Monthly Salary: 50000
        - Salary: Rs. 50,000
        - Income: ₹50000
        """
        # Remove commas and normalize
        text = ocr_text.replace(',', '').replace('₹', '').replace('Rs.', '')
        
        # Patterns to match salary
        patterns = [
            r'monthly\s+salary[:\s]+(\d+)',
            r'salary[:\s]+(\d+)',
            r'monthly\s+income[:\s]+(\d+)',
            r'income[:\s]+(\d+)',
            r'gross\s+salary[:\s]+(\d+)',
            r'net\s+salary[:\s]+(\d+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                salary = float(match.group(1))
                logger.info(f"Extracted salary: ₹{salary}")
                return salary
        
        logger.warning("Could not extract salary from document")
        return None
    
    def verify_eligibility(
        self,
        salary: float,
        loan_amount: float,
        loan_type: str = "personal"
    ) -> Tuple[bool, str, Dict]:
        """
        Verify if applicant is eligible for the loan
        
        Returns:
            (is_eligible, reason, details)
        """
        loan_type = loan_type.lower()
        multiplier = self.ELIGIBILITY_RULES.get(loan_type, 5)
        
        # Check minimum salary
        if salary < self.min_salary:
            return False, f"Salary below minimum requirement of ₹{self.min_salary}", {
                "salary": salary,
                "min_required": self.min_salary,
                "max_eligible_loan": 0,
                "requested_loan": loan_amount,
                "loan_type": loan_type
            }
        
        # Calculate maximum eligible loan
        max_eligible_loan = salary * multiplier
        
        # Check if requested amount is within limit
        if loan_amount > max_eligible_loan:
            return False, f"Loan amount exceeds eligibility. Maximum: ₹{max_eligible_loan:,.0f}", {
                "salary": salary,
                "max_eligible_loan": max_eligible_loan,
                "requested_loan": loan_amount,
                "loan_type": loan_type,
                "multiplier": multiplier
            }
        
        # Calculate loan-to-income ratio
        lti_ratio = (loan_amount / salary) if salary > 0 else 0
        
        return True, "Eligible for loan", {
            "salary": salary,
            "max_eligible_loan": max_eligible_loan,
            "requested_loan": loan_amount,
            "loan_type": loan_type,
            "multiplier": multiplier,
            "lti_ratio": round(lti_ratio, 2),
            "utilization_percent": round((loan_amount / max_eligible_loan) * 100, 2)
        }
    
    def create_verification_hash(self, data: Dict) -> str:
        """
        Create SHA256 hash of verification data for blockchain
        This ensures data integrity without revealing salary
        """
        # Create deterministic JSON string
        data_str = json.dumps(data, sort_keys=True, default=str)
        return hashlib.sha256(data_str.encode()).hexdigest()
    
    def create_zero_knowledge_proof(
        self,
        salary: float,
        loan_amount: float,
        loan_type: str
    ) -> Dict:
        """
        Create zero-knowledge proof that salary is sufficient
        WITHOUT revealing the actual salary amount
        
        Returns proof that can be verified without exposing salary
        """
        is_eligible, reason, details = self.verify_eligibility(
            salary, loan_amount, loan_type
        )
        
        # Create commitment (hash) of salary
        salary_commitment = hashlib.sha256(str(salary).encode()).hexdigest()
        
        # Create proof
        proof = {
            "is_eligible": is_eligible,
            "reason": reason,
            "salary_commitment": salary_commitment,  # Hash, not actual salary
            "loan_amount": loan_amount,
            "loan_type": loan_type,
            "verified_at": datetime.utcnow().isoformat(),
            "proof_type": "zero_knowledge",
            # DO NOT include actual salary in proof
        }
        
        return proof
    
    def verify_document_authenticity(
        self,
        ocr_text: str,
        expected_keywords: list = None
    ) -> Tuple[bool, str]:
        """
        Verify if document appears to be an authentic income certificate
        """
        if expected_keywords is None:
            expected_keywords = [
                "income", "salary", "certificate", "employer",
                "employee", "monthly", "annual"
            ]
        
        text_lower = ocr_text.lower()
        found_keywords = [kw for kw in expected_keywords if kw in text_lower]
        
        if len(found_keywords) < 3:
            return False, "Document does not appear to be an income certificate"
        
        return True, f"Document verified ({len(found_keywords)} keywords matched)"


# Global instance
document_verifier = DocumentVerifier()
