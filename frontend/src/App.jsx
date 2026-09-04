import ProctoringStatus from "./components/ProctoringStatus";
import { useEffect, useState } from "react";

import CameraFeed from "./components/CameraFeed";
import StatsPanel from "./components/StatsPanel";
import SessionPanel from "./components/SessionPanel";
import BlockchainVerification from "./components/BlockchainVerification";
import BlockchainHistory from "./components/BlockchainHistory";

import {
    getAIStatus,
    getProctoringEvents
} from "./services/api";

import "./App.css";

function App() {
    const [aiStatus, setAIStatus] = useState({
        count: 0,
        detections: [],
        highest_class: "N/A",
        highest_confidence: 0,
        processing_time: 0
    });
    
    const [proctoringStatus, setProctoringStatus] = useState({
        risk_score: 0,
        risk_level: "LOW",
        event_count: 0,
        events: []
    });

    useEffect(() => {
        const fetchStatus = async () => {
            try {
                const aiData = await getAIStatus();
                setAIStatus(aiData);

                const proctoringData = await getProctoringEvents();
                setProctoringStatus(proctoringData);
            } catch (error) {
                console.error("Failed to fetch monitoring status:", error);
            }
        };

        fetchStatus();
        const interval = setInterval(fetchStatus, 1000);
        return () => clearInterval(interval);
    }, []);
    
    return (
        <div className="app">
            <header className="header">
                <div>
                    <h1>EduView</h1>
                    <p>AI-Based Smart Online Examination Proctoring System</p>
                </div>
                <div className="system-status">
                    <span className="status-dot online-dot"></span>
                    System Online
                </div>
            </header>

            <main className="dashboard">
                {/* Cleanly renders the Session Panel once */}
                <SessionPanel />

                <CameraFeed />
                
                <ProctoringStatus proctoringStatus={proctoringStatus} />

                <StatsPanel aiStatus={aiStatus} />

                <div className="risk-section">
                    <h2>Proctoring Risk</h2>
                    <div className="risk-card">
                        <div>
                            <span className="stat-label">Risk Score</span>
                            <span className="risk-score">{proctoringStatus.risk_score}</span>
                        </div>
                        <div>
                            <span className="stat-label">Risk Level</span>
                            <span className={`risk-level ${proctoringStatus.risk_level.toLowerCase()}`}>
                                {proctoringStatus.risk_level}
                            </span>
                        </div>
                        <div>
                            <span className="stat-label">Events</span>
                            <span className="risk-score">{proctoringStatus.event_count}</span>
                        </div>
                    </div>
                </div>

                <BlockchainVerification />

                <BlockchainHistory />
                
                <div className="detection-section">
                    <h2>Proctoring Event History</h2>
                    {proctoringStatus.events && proctoringStatus.events.length > 0 ? (
                        <div className="detections">
                            {proctoringStatus.events
                                .slice()
                                .reverse()
                                .map((event) => (
                                <div className="detection-item" key={event.id}>
                                    <div>
                                        <strong>{event.event}</strong>
                                        <div className="event-time">
                                            {new Date(event.timestamp).toLocaleTimeString()}
                                        </div>
                                    </div>
                                    <div className="event-details">
                                        <span>{event.confidence.toFixed(1)}%</span>
                                        <span className={`severity ${event.severity.toLowerCase()}`}>
                                            {event.severity}
                                        </span>
                                        <span>+{event.risk_points}</span>
                                    </div>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <div className="no-detections">
                            No suspicious behaviour detected.
                        </div>
                    )}
                </div>
            </main>

            <footer>
                <p>AI + Blockchain Online Exam Integrity Platform</p>
            </footer>
        </div>
    );
}

export default App;