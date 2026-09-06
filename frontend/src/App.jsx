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

                const proctoringData =
                    await getProctoringEvents();

                setProctoringStatus(proctoringData);

            } catch (error) {

                console.error(
                    "Failed to fetch monitoring status:",
                    error
                );

            }

        };

        fetchStatus();

        const interval = setInterval(
            fetchStatus,
            1000
        );

        return () => clearInterval(interval);

    }, []);

    return (

        <div className="app">

            {/* HEADER */}

            <header className="header">

                <div>

                    <h2>
                        Blockchain and AI Framework for Online Exam Integrity
                    </h2>

                </div>

                <div className="system-status">

                    <span className="status-dot online-dot"></span>

                    System Online

                </div>

            </header>


            {/* MAIN DASHBOARD */}

            <main className="dashboard">

                {/* EXAM SESSION */}

                <SessionPanel />


                {/* CAMERA */}

                <CameraFeed />


                {/* LIVE PROCTORING STATUS */}

                <ProctoringStatus
                    proctoringStatus={proctoringStatus}
                />


                {/* AI STATISTICS */}

                <StatsPanel
                    aiStatus={aiStatus}
                />


                {/* BLOCKCHAIN VERIFICATION */}

                <BlockchainVerification />


                {/* BLOCKCHAIN HISTORY */}

                <BlockchainHistory />

            </main>


            {/* FOOTER */}

            <footer>

                <p>
                    AI + Blockchain Online Exam Integrity
                    Platform
                </p>

            </footer>

        </div>

    );
}

export default App;