// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

contract MicroPayment {
    // The address of the service provider (who can withdraw funds)
    address public owner;

    // Event to log each payment
    event Payment(address indexed from, uint256 amount);

    // UPDATED CONSTRUCTOR: Takes an address as input
    constructor(address _ownerAddress) {
        owner = _ownerAddress;
    }

    // Function for users to send payments
    function pay() external payable {
        require(msg.value > 0, "Payment must be greater than 0");
        emit Payment(msg.sender, msg.value);
    }

    // Function for the owner to withdraw all funds
    function withdraw() external {
        require(msg.sender == owner, "Only owner can withdraw");
        
        uint256 balance = address(this).balance;
        require(balance > 0, "No funds to withdraw");

        // Transfer the balance to the owner
        payable(owner).transfer(balance);
    }

    // A helper function to check the contract's balance
    function getBalance() external view returns (uint256) {
        return address(this).balance;
    }
}