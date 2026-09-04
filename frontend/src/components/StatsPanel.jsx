function StatsPanel({ aiStatus }) {

    return (
        <div className="stats-section">

            <h2>AI Detection Statistics</h2>

            <div className="stats-grid">

                <div className="stat-card">
                    <span className="stat-label">
                        Detections
                    </span>

                    <span className="stat-value">
                        {aiStatus.count}
                    </span>
                </div>

                <div className="stat-card">
                    <span className="stat-label">
                        Behaviour
                    </span>

                    <span className="stat-value behaviour">
                        {aiStatus.highest_class}
                    </span>
                </div>

                <div className="stat-card">
                    <span className="stat-label">
                        Confidence
                    </span>

                    <span className="stat-value">
                        {aiStatus.highest_confidence.toFixed(1)}%
                    </span>
                </div>

                <div className="stat-card">
                    <span className="stat-label">
                        Processing Time
                    </span>

                    <span className="stat-value">
                        {aiStatus.processing_time.toFixed(3)}s
                    </span>
                </div>

            </div>

        </div>
    );
}

export default StatsPanel;