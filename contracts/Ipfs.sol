// SPDX-License-Identifier: MIT

pragma solidity ^0.8.1;

contract Ipfs {
    mapping (address => string) public ipfsHashes;

    function addHash(string memory _ipfsHash) public {
        ipfsHashes[msg.sender] = _ipfsHash;
    }

    function getHash(address _address) public view returns (string memory) {
        return ipfsHashes[_address];
    }
}
