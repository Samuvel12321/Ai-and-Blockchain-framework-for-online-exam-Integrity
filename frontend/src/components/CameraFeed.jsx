import { useState, useEffect } from "react";
import { getVideoFeedURL, getCameraStatus } from "../services/api";

function CameraFeed() {
    const [cameraRunning, setCameraRunning] = useState(false);
    const [error, setError] = useState("");

    useEffect(() => {
        const checkStatus = async () => {
            try {
                const data = await getCameraStatus();

                if (
                    data.running === true ||
                    data.active === true ||
                    data.status === "active" ||
                    data.status === "running"
                ) {
                    setCameraRunning(true);
                    setError("");
                } else if (
                    data.running === false ||
                    data.active === false ||
                    data.status === "inactive" ||
                    data.status === "stopped"
                ) {
                    setCameraRunning(false);
                }
            } catch (err) {
                // Keep the UI stable if backend is temporarily unavailable.
            }
        };

        checkStatus();

        const interval = setInterval(checkStatus, 1000);

        return () => clearInterval(interval);
    }, []);

    return (
        <div className="camera-section">

            <div className="camera-header">

                <h2>Live Proctoring Camera</h2>

                <div
                    className={`status ${
                        cameraRunning ? "online" : "offline"
                    }`}
                >
                    <span className="status-dot"></span>

                    {cameraRunning
                        ? "Camera Active"
                        : "Camera Offline"}
                </div>

            </div>

            <div className="camera-container">

                {cameraRunning ? (

                    <img
                        src={getVideoFeedURL()}
                        alt="Live Proctoring Feed"
                        className="camera-feed"
                    />

                ) : (

                    <div className="camera-placeholder">

                        <div className="camera-icon">
                            📹
                        </div>

                        <h3>Camera is Off</h3>

                        <p>
                            Start the examination to activate
                            the proctoring camera.
                        </p>

                    </div>

                )}

            </div>

            {error && (
                <div className="error-message">
                    {error}
                </div>
            )}

        </div>
    );
}

export default CameraFeed;