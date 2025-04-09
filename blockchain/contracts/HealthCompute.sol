// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract HealthCompute {
    struct Computation {
        bytes32 dataHash;
        bytes32 resultHash;
        uint256 timestamp;
    }

    mapping(bytes32 => Computation) public computations;
    event ComputationLogged(bytes32 indexed dataHash, bytes32 resultHash);

    function logComputation(
        bytes32 _dataHash,
        bytes32 _resultHash
    ) public {
        computations[_dataHash] = Computation({
            dataHash: _dataHash,
            resultHash: _resultHash,
            timestamp: block.timestamp
        });
        emit ComputationLogged(_dataHash, _resultHash);
    }

    function verifyComputation(
        bytes32 _dataHash,
        bytes32 _resultHash
    ) public view returns (bool) {
        return computations[_dataHash].resultHash == _resultHash;
    }

    function verifyComputation(
    bytes32 _dataHash,
    bytes32 _resultHash
) public view returns (bool) {
    return computations[_dataHash].resultHash == _resultHash;
}
}