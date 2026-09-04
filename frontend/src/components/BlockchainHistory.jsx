import { useEffect, useState } from "react";
import { getBlockchainHistory } from "../services/api";

function BlockchainHistory() {
    const [sessions, setSessions] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    const loadHistory = async () => {
        try {
            setLoading(true);
            setError("");
            const data = await getBlockchainHistory();
            setSessions(data.sessions || []);
        } catch (err) {
            console.error("Failed to load blockchain history:", err);
            setError("Unable to load blockchain exam history.");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadHistory();
    }, []);

    if (loading) {
        return (
            <div className="blockchain-history">
                <h2>Blockchain Exam History</h2>
                <div className="history-message">Loading exam history...</div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="blockchain-history">
                <h2>Blockchain Exam History</h2>
                <div className="history-error">{error}</div>
            </div>
        );
    }

    return (
        <div className="blockchain-history">
            <div className="history-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                <div>
                    <h2>Blockchain Exam History</h2>
                    <p>Completed examinations and blockchain integrity verification.</p>
                </div>
                <button className="refresh-history-button" onClick={loadHistory} style={{ padding: '8px 16px', cursor: 'pointer' }}>
                    ↻ Refresh
                </button>
            </div>

            {sessions.length === 0 ? (
                <div className="history-message">No completed examinations found.</div>
            ) : (
                <div className="history-table-container" style={{ overflowX: 'auto', background: '#fff', borderRadius: '8px', border: '1px solid #ddd' }}>
                    <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
                        <thead style={{ backgroundColor: '#f9fafb', borderBottom: '2px solid #eee' }}>
                            <tr>
                                <th style={{ padding: '12px' }}>Session ID</th>
                                <th style={{ padding: '12px' }}>Date</th>
                                <th style={{ padding: '12px' }}>Duration</th>
                                <th style={{ padding: '12px' }}>Risk</th>
                                <th style={{ padding: '12px' }}>Integrity</th>
                                <th style={{ padding: '12px' }}>Tx Hash</th>
                            </tr>
                        </thead>
                        <tbody>
                            {sessions.map((session) => (
                                <tr key={session.session_id} style={{ borderBottom: '1px solid #eee' }}>
                                    <td style={{ padding: '12px', fontFamily: 'monospace' }}>
                                        {session.session_id.substring(0, 8)}...
                                    </td>
                                    <td style={{ padding: '12px' }}>
                                        {session.started_at ? new Date(session.started_at).toLocaleString() : "N/A"}
                                    </td>
                                    <td style={{ padding: '12px' }}>
                                        {session.duration ?? 0}s
                                    </td>
                                    <td style={{ padding: '12px' }}>
                                        <span className={`risk-level ${session.risk_level?.toLowerCase() || ''}`} style={{ fontWeight: 'bold' }}>
                                            {session.risk_level || "N/A"}
                                        </span>
                                    </td>
                                    <td style={{ padding: '12px' }}>
                                        {session.integrity === "VERIFIED" ? (
                                            <span style={{ color: 'green', fontWeight: 'bold' }}>✓ VERIFIED</span>
                                        ) : (
                                            <span style={{ color: 'red', fontWeight: 'bold' }}>⚠ TAMPERED</span>
                                        )}
                                    </td>
                                    <td style={{ padding: '12px', fontFamily: 'monospace', fontSize: '0.85em', color: '#666' }}>
                                        {session.blockchain?.transaction_hash ? session.blockchain.transaction_hash.substring(0, 10) + '...' : "N/A"}
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
}

export default BlockchainHistory;