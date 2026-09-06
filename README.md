### **AI \& Blockchain Framework for Online Exam Integrity**



An end-to-end smart online proctoring framework combining real-time computer vision, deep learning behavioral analysis, and decentralized tamper-proof blockchain audit trails to guarantee exam integrity.



##### 

##### 📌 **System Architecture**



&#x20;                          ┌─────────────────────────────┐

&#x20;                          │     Student Webcam Feed               │

&#x20;                          └──────────────┬──────────────┘

&#x20;                                         │

&#x20;                                         ▼

&#x20;                          ┌─────────────────────────────┐

&#x20;                          │      AI Proctoring Engine             │

&#x20;                          │        - YOLO Object / Pose           │

&#x20;                          │        - MediaPipe Face Mesh          │

&#x20;                          │        - Eye Gaze \& Tracking CNN      │ 

&#x20;                          └──────────────┬──────────────┘

&#x20;                                              │

&#x20;                                              ▼

┌───────────────────────────┐    REST / SSE       ┌─────────────────────────────┐

│    React / Vite Frontend           │ ◄────────────► │     Flask Backend API            	    │

│      - Live Proctor Dashboard      │                     │       - Camera Service           	    │

│      - Violation Alerts            │                     │       - Session Manager          	    │

│      - Blockchain Verification     │                     │       - Violation Aggregator     	    │

└───────────────────────────┘                     └──────────────┬──────────────┘

&#x09;						                        │ Session Finalization /

&#x20;    								                │ Risk Digest Hashing

&#x20;      								        	▼

&#x09;						   ┌─────────────────────────────┐

&#x09;						   │   Ethereum / EVM Blockchain 	   │

&#x09;						   │     (ExamIntegrity.sol)     	   │

&#x09;						   │  - Session \& Student Hash   	   │

&#x09;						   │  - Immutable Risk Score     	   │

&#x09;						   │  - Block Timestamp Audit    	   │

&#x09;						   └─────────────────────────────┘







##### 🚀 **Key Features**



###### **1. Multi-Modal AI Proctoring Engine**

* **Head Movement \& Suspicious Pose Detection:** YOLO-based tracking flags improper head turns, absent candidates, or multiple individuals in frame.
* **Prohibited Object Detection:** Spots unauthorized objects such as secondary smartphones, notes, and electronic devices.
* **Silent Cheating \& Gaze Tracking:** MediaPipe Face Mesh and CNN models analyze gaze direction, erratic saccades, and prolonged eye deviations away from the active exam screen.



###### **2. Microservice Backend \& Interactive UI**

* **Flask REST API:** Manages active exam sessions, handles real-time frame evaluation, and computes risk scores.
* **React + Vite Dashboard:** Displays low-latency live camera streaming, dynamic violation thresholds, status indicators, and session summaries.



**3. Immutable Blockchain Audit Trail**

\* \*\*Tamper-Proof Verification:\*\* Session violation logs and cumulative risk metrics are hashed and anchored to an EVM smart contract (`ExamIntegrity.sol`).

\* \*\*On-Chain Audit:\*\* Eliminates administrative record tampering; anyone with the session ID can independently verify exam integrity against on-chain block data.







#### 📁 **Repository Structure**



AI \& Blockchain Framework for Online Exam Integrity Folder

├── backend/

│   ├── app.py                      # Flask REST API entry point

│   ├── ai\_engine.py                # Computer vision and model inference engine

│   ├── camera\_service.py           # Video capture and frame streaming service

│   ├── database.py                 # Persistent session and violation storage

│   ├── exam\_session.py             # Active session lifecycle handler

│   ├── proctoring\_manager.py       # Detection coordinator and rule processor

│   ├── session\_manager.py          # Multi-candidate session management

│   ├── violation\_logger.py         # Timestamped infraction logging

│   └── services/

│       └── blockchain\_service.py   # Web3.py RPC client \& contract interaction

│

├── frontend/

│   ├── src/

│   │   ├── components/

│   │   │   ├── CameraFeed.jsx             # Live proctored video feed

│   │   │   ├── ProctoringStatus.jsx       # Real-time infraction notifications

│   │   │   ├── BlockchainHistory.jsx      # Historical ledger lookup

│   │   │   └── BlockchainVerification.jsx # On-chain hash audit verification

│   │   ├── App.jsx                        # Main React application layout

│   │   └── services/api.js                # Backend API communication layer

│   ├── package.json

│   └── vite.config.js

│

├── contracts/

│   └── ExamIntegrity.sol           # Solidity smart contract for immutable logs

│

├── object\_cheating/

│   ├── models/                     # Deep learning weights (YOLO, Face Landmarker)

│   └── utils/

│       └── eye\_tracker.py          # MediaPipe eye-gaze extraction routines

│

├── .gitignore

├── requirements.txt

└── README.md

⛓️ **Smart Contract Specifications**

Contract File: contracts/ExamIntegrity.sol



Solidity Version: ^0.8.20



Deployed Network: Ganache(EVM compatible)



Deployed Address: 0x2Ce49A3ec1Cf6Efb6A1A9f554394A38F186871D6



Core Functions

recordExam(sessionId, studentId, dataHash, riskScore, riskLevel): Anchors an immutable exam session summary.



getExam(sessionId): Retrieves on-chain verification metrics including timestamp, final risk score, and cryptographic hash.



##### 🛠️ **Installation \& Setup**

Prerequisites

Python 3.10 or 3.11



Node.js 18+ and npm



Access to an Ethereum RPC endpoint (Local Ganache)



**1. Backend Setup**



open command prompt:

\# Activate virtual environment



**# Windows:**

venv\\Scripts\\activate

**# Linux/macOS:**

source venv/bin/activate



**# Install dependencies**

pip install -r requirements.txt



**# Start Flask backend (default port 5000)**

python backend/app.py



**2. Frontend Setup**



**open command prompt:**

cd frontend



**# Install Node dependencies**

npm install



**# Run Vite development server**

npm run dev



Open http://localhost:5173 in your browser to access the proctoring dashboard.



##### 📜 **License**

This project is licensed under the MIT License.



