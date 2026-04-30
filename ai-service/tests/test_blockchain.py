"""
Tests for blockchain integration
"""

import pytest
from app.blockchain.contract import BlockchainService


@pytest.mark.asyncio
class TestBlockchain:
    """Test blockchain service functionality"""
    
    def test_blockchain_initialization(self):
        """Test blockchain service initialization"""
        service = BlockchainService()
        # Should initialize without errors
        assert service is not None
    
    def test_hash_data(self):
        """Test data hashing function"""
        service = BlockchainService()
        
        data1 = {"key": "value", "number": 123}
        data2 = {"number": 123, "key": "value"}  # Same data, different order
        
        hash1 = service._hash_data(data1)
        hash2 = service._hash_data(data2)
        
        # Hashes should be identical (order-independent)
        assert hash1 == hash2
        assert hash1.startswith("0x")
    
    def test_hash_data_different(self):
        """Test that different data produces different hashes"""
        service = BlockchainService()
        
        data1 = {"key": "value1"}
        data2 = {"key": "value2"}
        
        hash1 = service._hash_data(data1)
        hash2 = service._hash_data(data2)
        
        assert hash1 != hash2
    
    @pytest.mark.asyncio
    async def test_record_verification_disabled(self):
        """Test recording when blockchain is disabled"""
        service = BlockchainService()
        service.enabled = False
        
        result = await service.record_verification(
            verification_id="test-123",
            user_id="user-456",
            verification_data={"status": "approved"},
            status="approved"
        )
        
        # Should return None when disabled
        assert result is None
    
    def test_verify_data_integrity(self):
        """Test data integrity verification"""
        service = BlockchainService()
        
        original_data = {"creditScore": 720, "status": "approved"}
        data_hash = service._hash_data(original_data)
        
        # Verify with same data
        assert service.verify_data_integrity(original_data, data_hash) is True
        
        # Verify with tampered data
        tampered_data = {"creditScore": 800, "status": "approved"}
        assert service.verify_data_integrity(tampered_data, data_hash) is False
