function ProctoringStatus({ proctoringStatus }) {

    const status = proctoringStatus?.status || "NORMAL";

    const getStatusClass = () => {

        if (status === "SUSPICIOUS") {
            return "status-suspicious";
        }

        if (status === "WARNING") {
            return "status-warning";
        }

        return "status-normal";
    };

    const getStatusIcon = () => {

        if (status === "SUSPICIOUS") {
            return "🔴";
        }

        if (status === "WARNING") {
            return "🟠";
        }

        return "🟢";
    };

    return (
        <div className="proctoring-status-section">

            <div className="proctoring-status-header">
                <h2>Live Proctoring Status</h2>

                <span className={`proctoring-badge ${getStatusClass()}`}>
                    {getStatusIcon()} {status}
                </span>
            </div>

            <div className="proctoring-status-grid">

                <div className="proctoring-info">

                    <span className="info-label">
                        Detected Behaviour
                    </span>

                    <span className="info-value">
                        {proctoringStatus?.behaviour || "N/A"}
                    </span>

                </div>


                <div className="proctoring-info">

                    <span className="info-label">
                        Confidence
                    </span>

                    <span className="info-value">
                        {Number(
                            proctoringStatus?.confidence || 0
                        ).toFixed(2)}%
                    </span>

                </div>


                <div className="proctoring-info">

                    <span className="info-label">
                        Severity
                    </span>

                    <span className="info-value">
                        {proctoringStatus?.severity ?? 0}
                    </span>

                </div>

            </div>

        </div>
    );
}

export default ProctoringStatus;