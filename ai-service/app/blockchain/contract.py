"""
Blockchain integration for immutable audit trail
Stores loan verification records on Ethereum-compatible blockchain
"""

import json
import logging
from typing import Optional, Dict, Any
from datetime import datetime
from web3 import Web3
from web3.middleware import geth_poa_middleware
from eth_account import Account
from app.config.settings import settings

logger = logging.getLogger("verity-ai.blockchain")


# Smart Contract ABI (Solidity interface)
LOAN_VERIFICATION_ABI = [
    {
        "inputs": [
            {"internalType": "string", "name": "_verificationId", "type": "string"},
            {"internalType": "string", "name": "_userId", "type": "string"},
            {"internalType": "string", "name": "_dataHash", "type": "string"},
            {"internalType": "string", "name": "_status", "type": "string"},
            {"internalType": "uint256", "name": "_timestamp", "type": "uint256"}
        ],
        "name": "recordVerification",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "string", "name": "_verificationId", "type": "string"}],
        "name": "getVerification",
        "outputs": [
            {"internalType": "string", "name": "userId", "type": "string"},
            {"internalType": "string", "name": "dataHash", "type": "string"},
            {"internalType": "string", "name": "status", "type": "string"},
            {"internalType": "uint256", "name": "timestamp", "type": "uint256"},
            {"internalType": "bool", "name": "exists", "type": "bool"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "string", "name": "_verificationId", "type": "string"},
            {"internalType": "string", "name": "_newStatus", "type": "string"}
        ],
        "name": "updateStatus",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "string", "name": "verificationId", "type": "string"},
            {"indexed": True, "internalType": "string", "name": "userId", "type": "string"},
            {"indexed": False, "internalType": "string", "name": "status", "type": "string"},
            {"indexed": False, "internalType": "uint256", "name": "timestamp", "type": "uint256"}
        ],
        "name": "VerificationRecorded",
        "type": "event"
    }
]


class BlockchainService:
    """Service for blockchain interactions"""
    
    def __init__(self):
        self.enabled = settings.enable_blockchain
        self.w3: Optional[Web3] = None
        self.contract = None
        self.account = None
        
        if self.enabled:
            self._initialize()
    
    def _initialize(self):
        """Initialize Web3 connection and contract"""
        try:
            # Connect to blockchain network
            self.w3 = Web3(Web3.HTTPProvider(settings.blockchain_rpc_url))
            
            # Add PoA middleware for networks like Ganache
            if settings.blockchain_network in ["ganache", "polygon", "bsc"]:
                self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
            
            # Check connection
            if not self.w3.is_connected():
                logger.error("Failed to connect to blockchain network")
                self.enabled = False
                return
            
            # Setup account
            if settings.blockchain_private_key:
                self.account = Account.from_key(settings.blockchain_private_key)
                logger.info(f"Blockchain account: {self.account.address}")
            
            # Load contract
            if settings.contract_address:
                self.contract = self.w3.eth.contract(
                    address=Web3.to_checksum_address(settings.contract_address),
                    abi=LOAN_VERIFICATION_ABI
                )
                logger.info(f"✅ Blockchain service initialized: {settings.blockchain_network}")
            else:
                logger.warning("Contract address not configured")
                
        except Exception as e:
            logger.error(f"Blockchain initialization failed: {e}")
            self.enabled = False
    
    def _hash_data(self, data: Dict[Any, Any]) -> str:
        """Create SHA256 hash of verification data"""
        data_str = json.dumps(data, sort_keys=True, default=str)
        return Web3.keccak(text=data_str).hex()
    
    async def record_verification(
        self,
        verification_id: str,
        user_id: str,
        verification_data: Dict[Any, Any],
        status: str
    ) -> Optional[str]:
        """
        Record loan verification on blockchain
        Returns transaction hash if successful
        """
        if not self.enabled or not self.contract or not self.account:
            logger.warning("Blockchain not enabled or not configured")
            return None
        
        try:
            # Hash the verification data
            data_hash = self._hash_data(verification_data)
            timestamp = int(datetime.utcnow().timestamp())
            
            # Build transaction
            nonce = self.w3.eth.get_transaction_count(self.account.address)
            
            transaction = self.contract.functions.recordVerification(
                verification_id,
                user_id,
                data_hash,
                status,
                timestamp
            ).build_transaction({
                'from': self.account.address,
                'nonce': nonce,
                'gas': 200000,
                'gasPrice': self.w3.eth.gas_price
            })
            
            # Sign transaction
            signed_txn = self.w3.eth.account.sign_transaction(
                transaction,
                private_key=self.account.key
            )
            
            # Send transaction
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            # Wait for receipt
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
            
            if receipt['status'] == 1:
                logger.info(f"✅ Verification recorded on blockchain: {tx_hash.hex()}")
                return tx_hash.hex()
            else:
                logger.error(f"Transaction failed: {tx_hash.hex()}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to record on blockchain: {e}")
            return None
    
    async def get_verification(self, verification_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve verification record from blockchain"""
        if not self.enabled or not self.contract:
            return None
        
        try:
            result = self.contract.functions.getVerification(verification_id).call()
            
            if result[4]:  # exists
                return {
                    "user_id": result[0],
                    "data_hash": result[1],
                    "status": result[2],
                    "timestamp": result[3],
                    "exists": result[4]
                }
            return None
            
        except Exception as e:
            logger.error(f"Failed to retrieve from blockchain: {e}")
            return None
    
    async def update_status(
        self,
        verification_id: str,
        new_status: str
    ) -> Optional[str]:
        """Update verification status on blockchain"""
        if not self.enabled or not self.contract or not self.account:
            return None
        
        try:
            nonce = self.w3.eth.get_transaction_count(self.account.address)
            
            transaction = self.contract.functions.updateStatus(
                verification_id,
                new_status
            ).build_transaction({
                'from': self.account.address,
                'nonce': nonce,
                'gas': 100000,
                'gasPrice': self.w3.eth.gas_price
            })
            
            signed_txn = self.w3.eth.account.sign_transaction(
                transaction,
                private_key=self.account.key
            )
            
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
            
            if receipt['status'] == 1:
                logger.info(f"✅ Status updated on blockchain: {tx_hash.hex()}")
                return tx_hash.hex()
            return None
            
        except Exception as e:
            logger.error(f"Failed to update status on blockchain: {e}")
            return None
    
    def verify_data_integrity(
        self,
        verification_data: Dict[Any, Any],
        blockchain_hash: str
    ) -> bool:
        """Verify data hasn't been tampered with"""
        current_hash = self._hash_data(verification_data)
        return current_hash == blockchain_hash


# Global blockchain service instance
blockchain_service = BlockchainService()
