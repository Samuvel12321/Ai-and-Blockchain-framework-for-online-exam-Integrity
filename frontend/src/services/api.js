const API_BASE = "http://localhost:5000";

export const startCamera = async () => {
    const response = await fetch(`${API_BASE}/api/camera/start`, {
        method: "POST",
    });

    return response.json();
};

export const stopCamera = async () => {
    const response = await fetch(`${API_BASE}/api/camera/stop`, {
        method: "POST",
    });

    return response.json();
};

export const getCameraStatus = async () => {
    const response = await fetch(`${API_BASE}/api/camera/status`);

    return response.json();
};

export const getAIStatus = async () => {
    const response = await fetch(`${API_BASE}/api/ai/status`);

    return response.json();
};

export const getVideoFeedURL = () => {
    return `${API_BASE}/video_feed`;
};

export const getProctoringStatus = async () => {
    const response = await fetch(
        `${API_BASE}/api/proctoring/status`
    );

    if (!response.ok) {
        throw new Error("Failed to fetch proctoring status");
    }

    return response.json();
};

export const getProctoringEvents = async () => {
    const response = await fetch(
        `${API_BASE}/api/proctoring/events`
    );

    if (!response.ok) {
        throw new Error("Failed to fetch proctoring events");
    }

    return response.json();
};

export const startExam = async () => {
    const response = await fetch(
        `${API_BASE}/api/exam/start`,
        {
            method: "POST",
        }
    );

    if (!response.ok) {
        throw new Error("Failed to start exam");
    }

    return response.json();
};


export const stopExam = async () => {
    const response = await fetch(
        `${API_BASE}/api/exam/stop`,
        {
            method: "POST",
        }
    );

    if (!response.ok) {
        throw new Error("Failed to stop exam");
    }

    return response.json();
};


export const getExamStatus = async () => {
    const response = await fetch(
        `${API_BASE}/api/exam/status`
    );

    if (!response.ok) {
        throw new Error("Failed to fetch exam status");
    }

    return response.json();
};

export const startSession = async () => {

    const response = await fetch(
        `${API_BASE}/api/session/start`,
        {
            method: "POST",
        }
    );

    return response.json();
};


export const endSession = async () => {

    const response = await fetch(
        `${API_BASE}/api/session/end`,
        {
            method: "POST",
        }
    );

    return response.json();
};


export const getSessionStatus = async () => {

    const response = await fetch(
        `${API_BASE}/api/session/status`
    );

    return response.json();
};


export const getSessionHistory = async () => {

    const response = await fetch(
        `${API_BASE}/api/session/history`
    );

    return response.json();
};


export const verifyBlockchainSession = async (sessionId) => {
    const response = await fetch(
        `${API_BASE}/api/blockchain/verify/${sessionId}`
    );

    return response.json();
};


export const getBlockchainHistory = async () => {

    const response = await fetch(
        `${API_BASE}/api/blockchain/history`
    );

    if (!response.ok) {
        throw new Error("Failed to fetch blockchain history");
    }

    return response.json();
};

