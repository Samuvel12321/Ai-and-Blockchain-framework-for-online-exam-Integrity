import { useEffect, useState } from "react";

import {
    startSession,
    endSession,
    getSessionStatus,
    startCamera,
    stopCamera
} from "../services/api";


function SessionPanel() {

    const [session, setSession] = useState(null);

    const [loading, setLoading] = useState(false);

    const [error, setError] = useState("");


    const fetchSession = async () => {

        try {

            const data = await getSessionStatus();

            if (data.active) {

                setSession(data.session);

            } else {

                setSession(null);

            }

        } catch (err) {

            console.error(
                "Failed to fetch session:",
                err
            );

        }

    };


    useEffect(() => {

        fetchSession();

        const interval = setInterval(
            fetchSession,
            1000
        );

        return () => clearInterval(interval);

    }, []);


    const handleStart = async () => {

        try {

            setLoading(true);

            setError("");

            const data = await startSession();


            if (data.status === "success") {

                setSession(data.session);

                const cameraData = await startCamera();

                if (cameraData.status !== "success") {

                    setError(
                        "Exam started, but camera failed to start."
                    );

                }

            } else {

                setError(
                    data.message ||
                    "Failed to start exam session"
                );

            }

        } catch (err) {

            setError(
                "Cannot connect to backend."
            );

        } finally {

            setLoading(false);

        }

    };


    const handleEnd = async () => {

        try {

            setLoading(true);

            setError("");

            const data = await endSession();


            if (data.status === "success") {

                await stopCamera();

                setSession(null);

                alert(
                    "Exam session completed successfully."
            );

            } else {

                setError(
                    data.message ||
                    "Failed to end session"
                );

            }

        } catch (err) {

            setError(
                "Cannot connect to backend."
            );

        } finally {

            setLoading(false);

        }

    };


    return (

        <div className="session-section">

            <div className="session-header">

                <div>

                    <h2>Exam Session</h2>

                    <p>
                        Control the current examination
                        session.
                    </p>

                </div>


                <div
                    className={`session-status ${
                        session
                            ? "session-active"
                            : "session-inactive"
                    }`}
                >

                    <span className="status-dot"></span>

                    {session
                        ? "Exam Active"
                        : "No Active Exam"}

                </div>

            </div>


            {session ? (

                <div className="session-content">

                    <div className="session-info">

                        <div>

                            <span>
                                Session ID
                            </span>

                            <strong>
                                {session.session_id}
                            </strong>

                        </div>


                        <div>

                            <span>
                                Started At
                            </span>

                            <strong>
                                {new Date(
                                    session.started_at
                                ).toLocaleString()}
                            </strong>

                        </div>


                        <div>

                            <span>
                                Events
                            </span>

                            <strong>
                                {session.event_count}
                            </strong>

                        </div>


                        <div>

                            <span>
                                Risk Score
                            </span>

                            <strong>
                                {session.risk_score}
                            </strong>

                        </div>


                        <div>

                            <span>
                                Risk Level
                            </span>

                            <strong>
                                {session.risk_level}
                            </strong>

                        </div>

                    </div>


                    <button
                        className="end-session-button"
                        onClick={handleEnd}
                        disabled={loading}
                    >

                        {loading
                            ? "Ending..."
                            : "■ End Examination"}

                    </button>

                </div>

            ) : (

                <div className="session-start">

                    <p>
                        No examination is currently
                        active.
                    </p>

                    <button
                        className="start-session-button"
                        onClick={handleStart}
                        disabled={loading}
                    >

                        {loading
                            ? "Starting..."
                            : "▶ Start Examination"}

                    </button>

                </div>

            )}


            {error && (

                <div className="error-message">

                    {error}

                </div>

            )}

        </div>

    );

}


export default SessionPanel;