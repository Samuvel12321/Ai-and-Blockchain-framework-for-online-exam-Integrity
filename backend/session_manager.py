import uuid
import hashlib
import json
from datetime import datetime

from database import database
from services.blockchain_service import blockchain_service


class SessionManager:

    def __init__(self):

        self.active_session = None


    def start_session(self):

        if self.active_session is not None:

            return {
                "status": "error",
                "message": "A session is already active",
                "session": self.active_session
            }


        session_id = str(uuid.uuid4())


        self.active_session = {

            "session_id": session_id,

            "status": "ACTIVE",

            "started_at": datetime.now().isoformat(),

            "ended_at": None,

            "duration": 0,

            "event_count": 0,

            "risk_score": 0,

            "risk_level": "LOW"

        }


        print("=" * 60)
        print("EXAM SESSION STARTED")
        print("=" * 60)

        print(
            "Session ID:",
            session_id
        )


        return {

            "status": "success",

            "message": "Exam session started",

            "session": self.active_session

        }


    def update_session(
        self,
        event_count,
        risk_score,
        risk_level
    ):

        if self.active_session is None:

            return


        self.active_session["event_count"] = (
            event_count
        )

        self.active_session["risk_score"] = (
            risk_score
        )

        self.active_session["risk_level"] = (
            risk_level
        )


    def _generate_session_hash(self, session):

        """
        Generate SHA-256 hash of the completed
        exam session data.

        This hash represents the integrity of
        the exam session recorded on blockchain.
        """

        hash_data = {

            "session_id": session["session_id"],

            "status": session["status"],

            "started_at": session["started_at"],

            "ended_at": session["ended_at"],

            "duration": session["duration"],

            "event_count": session["event_count"],

            "risk_score": session["risk_score"],

            "risk_level": session["risk_level"]

        }


        serialized_data = json.dumps(
            hash_data,
            sort_keys=True
        )


        data_hash = hashlib.sha256(
            serialized_data.encode("utf-8")
        ).hexdigest()


        return data_hash


    def verify_session_integrity(self, session_id):

        # ----------------------------------------------------
        # 1. Get session from MongoDB
        # ----------------------------------------------------

        session = database.get_session(session_id)

        if session is None:

            return {
                "success": False,
                "message": "Session not found"
            }


        # ----------------------------------------------------
        # 2. Get blockchain record
        # ----------------------------------------------------

        try:

            blockchain_record = (
                blockchain_service.get_exam(
                    session_id
                )
            )

        except Exception as e:

            return {
                "success": False,
                "message": "Failed to retrieve blockchain record",
                "error": str(e)
            }


        if not blockchain_record:

            return {
                "success": False,
                "message": "Session not found on blockchain"
            }


        # ----------------------------------------------------
        # 3. Recalculate hash from MongoDB session
        # ----------------------------------------------------

        calculated_hash = (
            self._generate_session_hash(
                session
            )
        )


        # ----------------------------------------------------
        # 4. Get original blockchain hash
        # ----------------------------------------------------

        blockchain_hash = (
            blockchain_record.get(
                "data_hash"
            )
        )


        # ----------------------------------------------------
        # 5. Compare hashes
        # ----------------------------------------------------

        is_valid = (
            calculated_hash == blockchain_hash
        )


        # ----------------------------------------------------
        # 6. Return verification result
        # ----------------------------------------------------

        if is_valid:

            verification_status = "VERIFIED"

        else:

            verification_status = "TAMPERED"


        return {

            "success": True,

            "session_id": session_id,

            "status": verification_status,

            "integrity_valid": is_valid,

            "calculated_hash": calculated_hash,

            "blockchain_hash": blockchain_hash,

            "blockchain": {

                "transaction_hash":
                    session.get(
                        "blockchain",
                        {}
                    ).get(
                        "transaction_hash"
                    ),

                "block_number":
                    session.get(
                        "blockchain",
                        {}
                    ).get(
                        "block_number"
                    ),

                "contract_address":
                    session.get(
                        "blockchain",
                        {}
                    ).get(
                        "contract_address"
                    )

            }

        }


    def end_session(self):

        if self.active_session is None:

            return {
                "status": "error",
                "message": "No active session"
            }


        # ----------------------------------------------------
        # 1. Mark session as completed
        # ----------------------------------------------------

        self.active_session["status"] = "COMPLETED"

        self.active_session["ended_at"] = (
            datetime.now().isoformat()
        )


        start_time = datetime.fromisoformat(
            self.active_session["started_at"]
        )


        end_time = datetime.fromisoformat(
            self.active_session["ended_at"]
        )


        duration = (
            end_time - start_time
        ).total_seconds()


        self.active_session["duration"] = round(
            duration,
            2
        )


        completed_session = (
            self.active_session.copy()
        )


        # ----------------------------------------------------
        # 2. Generate SHA-256 integrity hash
        # ----------------------------------------------------

        data_hash = self._generate_session_hash(
            completed_session
        )


        completed_session["data_hash"] = data_hash


        print("=" * 60)
        print("SESSION INTEGRITY HASH")
        print("=" * 60)

        print(
            "Data Hash:",
            data_hash
        )


        # ----------------------------------------------------
        # 3. Record session on blockchain
        # ----------------------------------------------------

        blockchain_result = {

            "success": False,

            "message": "Blockchain recording not attempted"

        }


        try:

            blockchain_result = (
                blockchain_service.record_exam(

                    completed_session["session_id"],

                    "STUDENT-UNKNOWN",

                    data_hash,

                    completed_session["risk_score"],

                    completed_session["risk_level"]

                )
            )


            if blockchain_result.get("success"):

                print(
                    "[Blockchain] Exam session recorded successfully"
                )

                print(
                    "[Blockchain] Transaction:",
                    blockchain_result.get(
                        "transaction_hash"
                    )
                )

                print(
                    "[Blockchain] Block:",
                    blockchain_result.get(
                        "block_number"
                    )
                )

            else:

                print(
                    "[Blockchain] Failed to record exam"
                )


        except Exception as e:

            print(
                "[Blockchain] Error:",
                str(e)
            )

            blockchain_result = {

                "success": False,

                "message": str(e)

            }


        # ----------------------------------------------------
        # 4. Add blockchain information to session
        # ----------------------------------------------------

        completed_session["blockchain"] = {

            "recorded": blockchain_result.get(
                "success",
                False
            ),

            "transaction_hash": blockchain_result.get(
                "transaction_hash"
            ),

            "block_number": blockchain_result.get(
                "block_number"
            ),

            "contract_address": blockchain_result.get(
                "contract_address"
            )

        }


        # ----------------------------------------------------
        # 5. NOW save the complete session to MongoDB
        # ----------------------------------------------------

        database.save_session(
            completed_session
        )


        print(
            "[Database] Complete session + blockchain data saved"
        )


        # ----------------------------------------------------
        # 6. Clear active session
        # ----------------------------------------------------

        self.active_session = None


        print("=" * 60)
        print("EXAM SESSION ENDED")
        print("=" * 60)

        print(
            "Session ID:",
            completed_session["session_id"]
        )

        print(
            "Duration:",
            completed_session["duration"],
            "seconds"
        )

        print(
            "Risk Score:",
            completed_session["risk_score"]
        )

        print(
            "Risk Level:",
            completed_session["risk_level"]
        )

        print(
            "Blockchain Recorded:",
            completed_session["blockchain"]["recorded"]
        )


        # ----------------------------------------------------
        # 7. Return final result
        # ----------------------------------------------------

        return {

            "status": "success",

            "message": "Exam session completed",

            "session": completed_session

        }


    def get_active_session(self):

        return self.active_session


    def get_session_history(self):

        return database.get_all_sessions()


    def is_active(self):

        return self.active_session is not None


session_manager = SessionManager()