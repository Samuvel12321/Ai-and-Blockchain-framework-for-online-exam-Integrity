import { useState, useEffect } from "react";
import { startCamera, stopCamera, getVideoFeedURL, getCameraStatus } from "../services/api";

function CameraFeed() {
    const [cameraRunning, setCameraRunning] = useState(false);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    // NEW: Auto-sync camera state with the backend
    useEffect(() => {
        const checkStatus = async () => {
            try {
                const data = await getCameraStatus();
                // Check if backend reports camera is active/running
                if (data.active === true || data.status === "active" || data.status === "running") {
                    setCameraRunning(true);
                } else if (data.active === false || data.status === "inactive" || data.status === "stopped") {
                    setCameraRunning(false);
                }
            } catch (err) {
                // Fails silently in background if backend isn't ready
            }
        };

        checkStatus();
        const interval = setInterval(checkStatus, 1500);
        return () => clearInterval(interval);
    }, []);

    const handleStart = async () => {
        try {
            setLoading(true);
            setError("");
            const data = await startCamera();
            if (data.status === "success") {
                setCameraRunning(true);
            } else {
                setError(data.message || "Failed to start camera");
            }
        } catch (err) {
            setError("Cannot connect to Flask backend.");
        } finally {
            setLoading(false);
        }
    };

    const handleStop = async () => {
        try {
            setLoading(true);
            await stopCamera();
            setCameraRunning(false);
        } catch (err) {
            setError("Failed to stop camera.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="camera-section">
            <div className="camera-header">
                <h2>Live Proctoring Camera</h2>
                <div className={`status ${cameraRunning ? "online" : "offline"}`}>
                    <span className="status-dot"></span>
                    {cameraRunning ? "Camera Active" : "Camera Offline"}
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
                        <div className="camera-icon">📹</div>
                        <h3>Camera is Off</h3>
                        <p>Start the camera to begin online exam monitoring.</p>
                    </div>
                )}
            </div>

            {error && <div className="error-message">{error}</div>}

            <div className="camera-controls">
                {!cameraRunning ? (
                    <button className="start-button" onClick={handleStart} disabled={loading}>
                        {loading ? "Starting..." : "▶ Start Camera"}
                    </button>
                ) : (
                    <button className="stop-button" onClick={handleStop} disabled={loading}>
                        {loading ? "Stopping..." : "■ Stop Camera"}
                    </button>
                )}
            </div>
        </div>
    );
}

export default CameraFeed;