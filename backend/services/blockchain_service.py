from web3 import Web3


class BlockchainService:
    
    def __init__(self):

        print("=" * 60)
        print("Initializing Blockchain Service")
        print("=" * 60)

        # Ganache RPC
        self.rpc_url = "http://127.0.0.1:7545"

        # Connect to Ganache
        self.web3 = Web3(
            Web3.HTTPProvider(self.rpc_url)
        )

        if self.web3.is_connected():

            print("[Blockchain] Connected to Ganache")

        else:

            print("[Blockchain] Failed to connect to Ganache")

        # Deployed smart contract
        self.contract_address = Web3.to_checksum_address(
            "0x2Ce49A3ec1Cf6Efb6A1A9f554394A38F186871D6"
        )

        # Contract ABI
        self.contract_abi = [

            {
                "inputs": [
                    {
                        "internalType": "string",
                        "name": "_sessionId",
                        "type": "string"
                    },
                    {
                        "internalType": "string",
                        "name": "_studentId",
                        "type": "string"
                    },
                    {
                        "internalType": "string",
                        "name": "_dataHash",
                        "type": "string"
                    },
                    {
                        "internalType": "uint256",
                        "name": "_riskScore",
                        "type": "uint256"
                    },
                    {
                        "internalType": "string",
                        "name": "_riskLevel",
                        "type": "string"
                    }
                ],
                "name": "recordExam",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },

            {
                "inputs": [
                    {
                        "internalType": "string",
                        "name": "_sessionId",
                        "type": "string"
                    }
                ],
                "name": "getExam",
                "outputs": [
                    {
                        "internalType": "string",
                        "name": "",
                        "type": "string"
                    },
                    {
                        "internalType": "string",
                        "name": "",
                        "type": "string"
                    },
                    {
                        "internalType": "string",
                        "name": "",
                        "type": "string"
                    },
                    {
                        "internalType": "uint256",
                        "name": "",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "",
                        "type": "uint256"
                    },
                    {
                        "internalType": "string",
                        "name": "",
                        "type": "string"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            }

        ]

        # Create contract object
        self.contract = self.web3.eth.contract(
            address=self.contract_address,
            abi=self.contract_abi
        )

        print(
            "[Blockchain] Contract:",
            self.contract_address
        )

        print("=" * 60)

    def get_exam(self, session_id):

        if not self.web3.is_connected():
            raise Exception(
                "Blockchain connection is not available"
            )

        result = self.contract.functions.getExam(
            session_id
        ).call()

        return {
            "session_id": result[0],
            "student_id": result[1],
            "data_hash": result[2],
            "timestamp": result[3],
            "risk_score": result[4],
            "risk_level": result[5]
        }

    def record_exam(
        self,
        session_id,
        student_id,
        data_hash,
        risk_score,
        risk_level
    ):

        if not self.web3.is_connected():

            raise Exception(
                "Blockchain connection is not available"
            )

        # ---------------------------------------------
        # ACCOUNT
        # ---------------------------------------------

        account = self.web3.eth.accounts[0]

        # ---------------------------------------------
        # BUILD TRANSACTION
        # ---------------------------------------------

        transaction = self.contract.functions.recordExam(
            session_id,
            student_id,
            data_hash,
            risk_score,
            risk_level
        ).build_transaction({

            "from": account,

            "nonce":
                self.web3.eth.get_transaction_count(
                    account
                ),

            "gas":
                300000,

            "gasPrice":
                self.web3.eth.gas_price

        })

        # ---------------------------------------------
        # SIGN TRANSACTION
        # ---------------------------------------------

        # For Ganache development only.
        #
        # We will later replace this with a proper
        # secure wallet/private-key configuration.

        private_key = "0x32895ca2e2aa8b4aacc501cba04833b044011259d18857e00466f403890c7a80"

        signed_transaction = self.web3.eth.account.sign_transaction(
            transaction,
            private_key=private_key
        )

        # ---------------------------------------------
        # SEND TRANSACTION
        # ---------------------------------------------

        tx_hash = self.web3.eth.send_raw_transaction(
            signed_transaction.raw_transaction
        )

        # ---------------------------------------------
        # WAIT FOR CONFIRMATION
        # ---------------------------------------------

        receipt = self.web3.eth.wait_for_transaction_receipt(
            tx_hash
        )

        return {
            "success": True,
            "transaction_hash": tx_hash.hex(),
            "block_number": receipt.blockNumber,
            "contract_address": self.contract_address
        }


# Global blockchain service
blockchain_service = BlockchainService()