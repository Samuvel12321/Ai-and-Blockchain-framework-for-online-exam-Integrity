import { useState } from "react";
import { verifyBlockchainSession } from "../services/api";

function BlockchainVerification() {

    const [sessionId, setSessionId] = useState("");
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const handleVerify = async () => {

        if (!sessionId.trim()) {
            setError("Please enter a session ID.");
            return;
        }

        try {

            setLoading(true);
            setError("");
            setResult(null);

            const data = await verifyBlockchainSession(
                sessionId.trim()
            );

            if (data.success) {
                setResult(data);
            } else {
                setError(
                    data.message ||
                    "Verification failed."
                );
            }

        } catch (err) {

            console.error(err);

            setError(
                "Unable to connect to the verification service."
            );

        } finally {

            setLoading(false);

        }
    };


    return (
        <div className="blockchain-section">

            <h2>Blockchain Integrity Verification</h2>

            <p>
                Verify that the exam session stored in the
                database matches the record stored on the blockchain.
            </p>

            <div className="verification-form">

                <input
                    type="text"
                    placeholder="Enter Session ID"
                    value={sessionId}
                    onChange={(e) =>
                        setSessionId(e.target.value)
                    }
                />

                <button
                    onClick={handleVerify}
                    disabled={loading}
                >
                    {loading
                        ? "Verifying..."
                        : "Verify Session"}
                </button>

            </div>


            {error && (
                <div className="verification-error">
                    {error}
                </div>
            )}


            {result && (

                <div
                    className={
                        result.integrity_valid
                            ? "verification-result verified"
                            : "verification-result tampered"
                    }
                >

                    <h3>
                        {result.integrity_valid
                            ? "✓ SESSION VERIFIED"
                            : "⚠ SESSION TAMPERED"}
                    </h3>


                    <div className="verification-details">

                        <p>
                            <strong>Session ID:</strong>{" "}
                            {result.session_id}
                        </p>

                        <p>
                            <strong>Status:</strong>{" "}
                            {result.status}
                        </p>

                        <p>
                            <strong>Blockchain Block:</strong>{" "}
                            {result.blockchain?.block_number ?? "N/A"}
                        </p>

                        <p>
                            <strong>Transaction:</strong>{" "}
                            {result.blockchain?.transaction_hash ?? "N/A"}
                        </p>

                        <p>
                            <strong>Calculated Hash:</strong>
                        </p>

                        <code>
                            {result.calculated_hash}
                        </code>

                        <p>
                            <strong>Blockchain Hash:</strong>
                        </p>

                        <code>
                            {result.blockchain_hash}
                        </code>

                    </div>

                </div>
            )}

        </div>
    );
}

export default BlockchainVerification;