import { useEffect, useState } from "react";
import { getBlockchainHistory } from "../services/api";

function BlockchainHistory() {
    const [sessions, setSessions] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [selectedSession, setSelectedSession] = useState(null);

    const loadHistory = async () => {
        try {
            setLoading(true);
            setError("");

            const data = await getBlockchainHistory();

            setSessions(data.sessions || []);
        } catch (err) {
            console.error(
                "Failed to load blockchain history:",
                err
            );

            setError(
                "Unable to load blockchain exam history."
            );
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadHistory();
    }, []);

    const getIntegrityStatus = (session) => {
        if (session.integrity === "VERIFIED") {
            return {
                label: "✓ VERIFIED",
                className: "verified"
            };
        }

        if (session.integrity === "TAMPERED") {
            return {
                label: "⚠ TAMPERED",
                className: "tampered"
            };
        }

        return {
            label: "— NOT VERIFIED",
            className: "not-verified"
        };
    };

    const formatDate = (date) => {
        if (!date) {
            return "N/A";
        }

        return new Date(date).toLocaleString();
    };

    const closeModal = () => {
        setSelectedSession(null);
    };

    return (
        <>
            <div className="blockchain-history">

                <div className="history-header">

                    <div>
                        <h2>Blockchain Verification Ledger</h2>

                        <p>
                            Completed examinations and blockchain
                            integrity verification.
                        </p>
                    </div>

                    <button
                        className="refresh-history-button"
                        onClick={loadHistory}
                        disabled={loading}
                    >
                        {loading ? "Refreshing..." : "↻ Refresh"}
                    </button>

                </div>

                {loading ? (
                    <div className="history-message">
                        Loading exam history...
                    </div>
                ) : error ? (
                    <div className="history-error">
                        {error}
                    </div>
                ) : sessions.length === 0 ? (
                    <div className="history-message">
                        No completed examinations found.
                    </div>
                ) : (

                    <div className="history-table-wrapper">

                        <table className="blockchain-history-table">

                            <thead>
                                <tr>
                                    <th>Session ID</th>
                                    <th>Date</th>
                                    <th>Duration</th>
                                    <th>Risk</th>
                                    <th>Integrity</th>
                                    <th>Action</th>
                                </tr>
                            </thead>

                            <tbody>

                                {sessions.map((session) => {

                                    const integrity =
                                        getIntegrityStatus(session);

                                    return (
                                        <tr
                                            key={session.session_id}
                                        >

                                            <td>
                                                <span className="table-session-id">
                                                    {session.session_id
                                                        ? `${session.session_id.substring(
                                                              0,
                                                              8
                                                          )}...`
                                                        : "N/A"}
                                                </span>
                                            </td>

                                            <td>
                                                {formatDate(
                                                    session.started_at
                                                )}
                                            </td>

                                            <td>
                                                {session.duration ?? 0}s
                                            </td>

                                            <td>
                                                <span
                                                    className={`table-risk ${
                                                        session.risk_level?.toLowerCase() ||
                                                        ""
                                                    }`}
                                                >
                                                    {session.risk_level ||
                                                        "N/A"}
                                                </span>
                                            </td>

                                            <td>
                                                <span
                                                    className={`table-integrity ${integrity.className}`}
                                                >
                                                    {integrity.label}
                                                </span>
                                            </td>

                                            <td>

                                                <button
                                                    className="view-details-button"
                                                    onClick={() =>
                                                        setSelectedSession(
                                                            session
                                                        )
                                                    }
                                                >
                                                    👁 View Details
                                                </button>

                                            </td>

                                        </tr>
                                    );
                                })}

                            </tbody>

                        </table>

                    </div>
                )}

            </div>


            {/* DETAILS MODAL */}

            {selectedSession && (

                <div
                    className="details-modal-overlay"
                    onClick={closeModal}
                >

                    <div
                        className="details-modal"
                        onClick={(event) =>
                            event.stopPropagation()
                        }
                    >

                        <div className="details-modal-header">

                            <div>
                                <h2>
                                    Examination Record
                                </h2>

                                <p>
                                    Complete session and blockchain
                                    verification details
                                </p>
                            </div>

                            <button
                                className="modal-close-button"
                                onClick={closeModal}
                                aria-label="Close"
                            >
                                ✕
                            </button>

                        </div>


                        <div className="details-modal-body">

                            {/* SESSION INFORMATION */}

                            <div className="modal-section">

                                <h3>
                                    Session Information
                                </h3>

                                <div className="modal-details-grid">

                                    <div className="modal-detail-item">
                                        <span>
                                            Session ID
                                        </span>

                                        <strong className="break-text">
                                            {selectedSession.session_id ||
                                                "N/A"}
                                        </strong>
                                    </div>

                                    <div className="modal-detail-item">
                                        <span>
                                            Status
                                        </span>

                                        <strong>
                                            {selectedSession.status ||
                                                "N/A"}
                                        </strong>
                                    </div>

                                    <div className="modal-detail-item">
                                        <span>
                                            Started At
                                        </span>

                                        <strong>
                                            {formatDate(
                                                selectedSession.started_at
                                            )}
                                        </strong>
                                    </div>

                                    <div className="modal-detail-item">
                                        <span>
                                            Ended At
                                        </span>

                                        <strong>
                                            {formatDate(
                                                selectedSession.ended_at
                                            )}
                                        </strong>
                                    </div>

                                    <div className="modal-detail-item">
                                        <span>
                                            Duration
                                        </span>

                                        <strong>
                                            {selectedSession.duration ??
                                                0}
                                            s
                                        </strong>
                                    </div>

                                </div>

                            </div>

                            {/* BLOCKCHAIN INFORMATION */}

                            <div className="modal-section">

                                <h3>
                                    Blockchain Information
                                </h3>

                                <div className="modal-details-grid">

                                    <div className="modal-detail-item">
                                        <span>
                                            Blockchain Status
                                        </span>

                                        <strong
                                            className={
                                                selectedSession
                                                    .blockchain
                                                    ?.recorded
                                                    ? "blockchain-success"
                                                    : "blockchain-failed"
                                            }
                                        >
                                            {selectedSession
                                                .blockchain
                                                ?.recorded
                                                ? "✓ RECORDED"
                                                : "✕ NOT RECORDED"}
                                        </strong>
                                    </div>

                                    <div className="modal-detail-item">
                                        <span>
                                            Block Number
                                        </span>

                                        <strong>
                                            {selectedSession
                                                .blockchain
                                                ?.block_number ??
                                                "N/A"}
                                        </strong>
                                    </div>

                                    <div className="modal-detail-item full-width">
                                        <span>
                                            Transaction Hash
                                        </span>

                                        <code>
                                            {selectedSession
                                                .blockchain
                                                ?.transaction_hash ||
                                                "N/A"}
                                        </code>
                                    </div>

                                    <div className="modal-detail-item full-width">
                                        <span>
                                            Contract Address
                                        </span>

                                        <code>
                                            {selectedSession
                                                .blockchain
                                                ?.contract_address ||
                                                "N/A"}
                                        </code>
                                    </div>

                                </div>

                            </div>


                            {/* INTEGRITY HASH */}

                            <div className="modal-section">

                                <h3>
                                    Integrity Verification
                                </h3>

                                <div className="integrity-hash-box">

                                    <span>
                                        SHA-256 Session Hash
                                    </span>

                                    <code>
                                        {selectedSession.data_hash ||
                                            "N/A"}
                                    </code>

                                </div>

                                <div
                                    className={`modal-verification-status ${
                                        getIntegrityStatus(
                                            selectedSession
                                        ).className
                                    }`}
                                >
                                    {
                                        getIntegrityStatus(
                                            selectedSession
                                        ).label
                                    }
                                </div>

                            </div>

                        </div>


                        <div className="details-modal-footer">

                            <button
                                className="modal-close-footer-button"
                                onClick={closeModal}
                            >
                                Close
                            </button>

                        </div>

                    </div>

                </div>

            )}

        </>
    );
}

export default BlockchainHistory;