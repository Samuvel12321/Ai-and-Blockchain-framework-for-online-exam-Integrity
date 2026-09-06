// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract ExamIntegrity {

    struct ExamRecord {
        string sessionId;
        string studentId;
        string dataHash;
        uint256 timestamp;
        uint256 riskScore;
        string riskLevel;
    }

    mapping(string => ExamRecord) private examRecords;

    event ExamRecorded(
        string indexed sessionId,
        string studentId,
        string dataHash,
        uint256 timestamp,
        uint256 riskScore,
        string riskLevel
    );

    function recordExam(
        string memory _sessionId,
        string memory _studentId,
        string memory _dataHash,
        uint256 _riskScore,
        string memory _riskLevel
    ) public {

        examRecords[_sessionId] = ExamRecord({
            sessionId: _sessionId,
            studentId: _studentId,
            dataHash: _dataHash,
            timestamp: block.timestamp,
            riskScore: _riskScore,
            riskLevel: _riskLevel
        });

        emit ExamRecorded(
            _sessionId,
            _studentId,
            _dataHash,
            block.timestamp,
            _riskScore,
            _riskLevel
        );
    }

    function getExam(
        string memory _sessionId
    )
        public
        view
        returns (
            string memory,
            string memory,
            string memory,
            uint256,
            uint256,
            string memory
        )
    {
        ExamRecord memory record = examRecords[_sessionId];

        return (
            record.sessionId,
            record.studentId,
            record.dataHash,
            record.timestamp,
            record.riskScore,
            record.riskLevel
        );
    }
}