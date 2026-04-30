"""
Tests for loan verification endpoints
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestVerification:
    """Test loan verification functionality"""
    
    async def test_quick_check_approve(
        self,
        authenticated_client: tuple[AsyncClient, dict],
        sample_loan_data: dict
    ):
        """Test quick eligibility check with approval"""
        client, _ = authenticated_client
        
        response = await client.post(
            "/api/verify/quick-check",
            json=sample_loan_data
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["recommendation"] == "approve"
        assert data["approvalScore"] > 70
        assert len(data["ruleChecks"]) > 0
    
    async def test_quick_check_reject(
        self,
        authenticated_client: tuple[AsyncClient, dict]
    ):
        """Test quick eligibility check with rejection"""
        client, _ = authenticated_client
        
        # Low credit score should trigger rejection
        response = await client.post(
            "/api/verify/quick-check",
            json={
                "loanType": "personal",
                "extractedData": {
                    "creditScore": 500,  # Below threshold
                    "monthlyIncome": 45000,
                    "age": 28,
                    "workExperienceYears": 3,
                    "debtToIncomeRatio": 0.30,
                    "loanAmount": 500000
                }
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["recommendation"] == "reject"
        assert data["approvalScore"] < 70
    
    async def test_quick_check_missing_data(
        self,
        authenticated_client: tuple[AsyncClient, dict]
    ):
        """Test quick check with missing required data"""
        client, _ = authenticated_client
        
        response = await client.post(
            "/api/verify/quick-check",
            json={
                "loanType": "personal",
                "extractedData": {
                    "creditScore": 720
                    # Missing other required fields
                }
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        # Should still process but with lower confidence
        assert "ruleChecks" in data
    
    async def test_quick_check_unauthorized(
        self,
        client: AsyncClient,
        sample_loan_data: dict
    ):
        """Test quick check without authentication"""
        response = await client.post(
            "/api/verify/quick-check",
            json=sample_loan_data
        )
        
        assert response.status_code == 401
    
    async def test_different_loan_types(
        self,
        authenticated_client: tuple[AsyncClient, dict]
    ):
        """Test verification for different loan types"""
        client, _ = authenticated_client
        
        loan_types = ["personal", "home", "auto", "business", "education"]
        
        for loan_type in loan_types:
            response = await client.post(
                "/api/verify/quick-check",
                json={
                    "loanType": loan_type,
                    "extractedData": {
                        "creditScore": 750,
                        "monthlyIncome": 50000,
                        "annualIncome": 600000,
                        "age": 30,
                        "workExperienceYears": 5,
                        "debtToIncomeRatio": 0.25,
                        "loanAmount": 1000000,
                        "propertyValue": 2000000,
                        "ltvRatio": 0.50,
                        "annualRevenue": 1000000,
                        "businessAgeYears": 3,
                        "averageMonthlyBalance": 50000
                    }
                }
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert "recommendation" in data


@pytest.mark.asyncio
class TestVerificationWithBlockchain:
    """Test verification with blockchain integration"""
    
    async def test_verification_blockchain_record(
        self,
        authenticated_client: tuple[AsyncClient, dict],
        sample_loan_data: dict,
        mock_blockchain_service
    ):
        """Test that verification is recorded on blockchain"""
        client, _ = authenticated_client
        
        response = await client.post(
            "/api/verify/quick-check",
            json=sample_loan_data
        )
        
        assert response.status_code == 200
        # In real implementation, check blockchain transaction hash
        # For now, just verify the response structure
        data = response.json()
        assert "recommendation" in data
