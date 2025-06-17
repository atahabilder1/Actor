// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

contract BuggyBank {
    mapping(address => uint256) public balances;
    address public owner;
    bool public locked;

    constructor() {
        owner = msg.sender;
    }

    // ❌ Access Control: No modifier to restrict critical function
    function setOwner(address newOwner) public {
        owner = newOwner;
    }

    // ❌ Reentrancy + ❌ State update after transfer
    function withdraw() public {
        uint256 amount = balances[msg.sender];
        if (amount > 0) {
            (bool success, ) = msg.sender.call{value: amount}(""); // 🛑 Reentrancy risk
            require(success, "Transfer failed");
            balances[msg.sender] = 0;
        }
    }

    // ❌ Integer Overflow (in older versions) — now for demonstration
    function unsafeAdd(uint256 a, uint256 b) public pure returns (uint256) {
        return a + b; // no SafeMath or unchecked
    }

    // ❌ Access Control missing on admin-only functionality
    function emergencyWithdraw() public {
        payable(msg.sender).transfer(address(this).balance);
    }

    // ❌ State variable locking logic flawed
    function lockContract() public {
        locked = true;
    }

    function deposit() public payable {
        require(!locked, "Contract is locked");
        balances[msg.sender] += msg.value;
    }

    // ❌ Public getter allows anyone to view owner (might be sensitive)
    function getOwner() public view returns (address) {
        return owner;
    }

    // ❌ Storage collision if used via delegatecall in upgradeable proxy (demo purpose)
    uint256 private dummy1;
    uint256 private dummy2;
}
