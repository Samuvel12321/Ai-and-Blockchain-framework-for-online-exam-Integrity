import { useState } from "react";

import { verifyBlockchainSession } from "../services/api";


function FinalResult({ session }) {

    const [verification, setVerification] = useState(null);
    const [verifying, setVerifying] = useState(false);
    const [error, setError] = useState("");


    if (!session) {
        return null;
    }


    const handleVerify = async () => {

        try {

            setVerifying(true);
            setError("");

            const result =
                await verifyBlockchainSession(
                    session.session_id
                );

            setVerification(result);

        } catch (err) {

            console.error(
                "Verification failed:",
                err
            );

            setError(
                "Unable to verify blockchain integrity."
            );

        } finally {

            setVerifying(false);

        }
    };


    const blockchain =
        session.blockchain || {};


    const isVerified =
        verification?.status === "VERIFIED";


    return (

        <div className="final-result">

            <div className="final-result-header">

                <div>

                    <h2>
                        Final Examination Result
                    </h2>

                    <p>
                        Blockchain-backed examination
                        integrity report
                    </p>

                </div>


                <div
                    className={`result-status ${
                        session.status === "COMPLETED"
                            ? "completed"
                            : ""
                    }`}
                >

                    ✓ {session.status}

                </div>

            </div>


            {/* SESSION INFORMATION */}

            <div className="result-section">

                <h3>
                    Examination Details
                </h3>


                <div className="result-grid">

                    <div className="result-item">

                        <span>
                            Session ID
                        </span>

                        <strong className="mono">
                            {session.session_id}
                        </strong>

                    </div>


                    <div className="result-item">

                        <span>
                            Duration
                        </span>

                        <strong>
                            {session.duration}s
                        </strong>

                    </div>


                    <div className="result-item">

                        <span>
                            AI Events
                        </span>

                        <strong>
                            {session.event_count ?? 0}
                        </strong>

                    </div>


                    <div className="result-item">

                        <span>
                            Risk Score
                        </span>

                        <strong>
                            {session.risk_score ?? 0}
                        </strong>

                    </div>


                    <div className="result-item">

                        <span>
                            Risk Level
                        </span>

                        <strong>
                            {session.risk_level || "N/A"}
                        </strong>

                    </div>


                    <div className="result-item">

                        <span>
                            Started
                        </span>

                        <strong>
                            {session.started_at || "N/A"}
                        </strong>

                    </div>


                    <div className="result-item">

                        <span>
                            Ended
                        </span>

                        <strong>
                            {session.ended_at || "N/A"}
                        </strong>

                    </div>

                </div>

            </div>


            {/* INTEGRITY */}

            <div className="result-section">

                <h3>
                    Session Integrity
                </h3>


                <div className="hash-box">

                    <span>
                        SHA-256 Hash
                    </span>

                    <code>
                        {session.data_hash || "N/A"}
                    </code>

                </div>

            </div>


            {/* BLOCKCHAIN */}

            <div className="result-section">

                <h3>
                    Blockchain Record
                </h3>


                <div className="result-grid">

                    <div className="result-item">

                        <span>
                            Blockchain Status
                        </span>

                        <strong
                            className={
                                blockchain.recorded
                                    ? "success-text"
                                    : "danger-text"
                            }
                        >

                            {blockchain.recorded
                                ? "Recorded"
                                : "Not Recorded"}

                        </strong>

                    </div>


                    <div className="result-item">

                        <span>
                            Block Number
                        </span>

                        <strong>
                            {blockchain.block_number ??
                                "N/A"}
                        </strong>

                    </div>


                    <div className="result-item">

                        <span>
                            Transaction Hash
                        </span>

                        <strong className="mono">

                            {blockchain.transaction_hash ||
                                "N/A"}

                        </strong>

                    </div>


                    <div className="result-item">

                        <span>
                            Contract Address
                        </span>

                        <strong className="mono">

                            {blockchain.contract_address ||
                                "N/A"}

                        </strong>

                    </div>

                </div>

            </div>


            {/* VERIFICATION */}

            <div className="verification-section">

                <div>

                    <h3>
                        Blockchain Integrity Verification
                    </h3>

                    {!verification && (
                        <p>
                            Verify that the exam data stored
                            in MongoDB matches the hash stored
                            on the blockchain.
                        </p>
                    )}

                    {verification && (

                        <div
                            className={
                                isVerified
                                    ? "verification-success"
                                    : "verification-failed"
                            }
                        >

                            {isVerified
                                ? "✓ INTEGRITY VERIFIED"
                                : "⚠ INTEGRITY CHECK FAILED"}

                        </div>

                    )}

                </div>


                <button
                    className="verify-button"
                    onClick={handleVerify}
                    disabled={verifying}
                >

                    {verifying
                        ? "Verifying..."
                        : "🔐 Verify Integrity"}

                </button>

            </div>


            {error && (

                <div className="verification-error">
                    {error}
                </div>

            )}

        </div>

    );
}


export default FinalResult;