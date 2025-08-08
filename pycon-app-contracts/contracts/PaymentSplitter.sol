// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract PaymentSplitter {
    struct Payment {
        string description;
        address[] recipients;
        uint256[] percentages;
        uint256 totalAmount;
        uint256 collectedAmount;
        bool isActive;
        address creator;
    }
    
    mapping(uint256 => Payment) public payments;
    mapping(uint256 => mapping(address => uint256)) public contributions;
    mapping(uint256 => mapping(address => bool)) public hasPaid;
    
    uint256 public nextPaymentId;
    
    event PaymentCreated(
        uint256 indexed paymentId, 
        string description, 
        address creator, 
        uint256 totalAmount
    );
    
    event ContributionMade(
        uint256 indexed paymentId, 
        address contributor, 
        uint256 amount
    );
    
    event PaymentCompleted(uint256 indexed paymentId);
    
    // Create a new payment split
    function createPayment(
        string memory _description,
        address[] memory _recipients,
        uint256[] memory _percentages,
        uint256 _totalAmount
    ) public {
        require(_recipients.length == _percentages.length, "Mismatched arrays");
        require(_recipients.length > 0, "Need at least one recipient");
        require(_totalAmount > 0, "Amount must be greater than 0");
        
        // Check percentages add up to 100
        uint256 totalPercentage = 0;
        for (uint i = 0; i < _percentages.length; i++) {
            totalPercentage += _percentages[i];
        }
        require(totalPercentage == 100, "Percentages must add up to 100");
        
        payments[nextPaymentId] = Payment({
            description: _description,
            recipients: _recipients,
            percentages: _percentages,
            totalAmount: _totalAmount,
            collectedAmount: 0,
            isActive: true,
            creator: msg.sender
        });
        
        emit PaymentCreated(nextPaymentId, _description, msg.sender, _totalAmount);
        nextPaymentId++;
    }
    
    // Pay your share of the bill
    function payInvoice(uint256 _paymentId) public payable {
        Payment storage payment = payments[_paymentId];
        require(payment.isActive, "Payment not active");
        require(!hasPaid[_paymentId][msg.sender], "Already paid");
        require(msg.value > 0, "Must send some CELO");
        
        contributions[_paymentId][msg.sender] = msg.value;
        hasPaid[_paymentId][msg.sender] = true;
        payment.collectedAmount += msg.value;
        
        emit ContributionMade(_paymentId, msg.sender, msg.value);
        
        // Check if we've collected enough to distribute
        if (payment.collectedAmount >= payment.totalAmount) {
            _distributePayment(_paymentId);
        }
    }
    
    // Internal function to distribute payments
    function _distributePayment(uint256 _paymentId) internal {
        Payment storage payment = payments[_paymentId];
        
        for (uint i = 0; i < payment.recipients.length; i++) {
            uint256 amount = (payment.totalAmount * payment.percentages[i]) / 100;
            payable(payment.recipients[i]).transfer(amount);
        }
        
        payment.isActive = false;
        emit PaymentCompleted(_paymentId);
    }
    
    // Get payment details
    function getPayment(uint256 _paymentId) public view returns (
        string memory description,
        address[] memory recipients,
        uint256[] memory percentages,
        uint256 totalAmount,
        uint256 collectedAmount,
        bool isActive,
        address creator
    ) {
        Payment memory payment = payments[_paymentId];
        return (
            payment.description,
            payment.recipients,
            payment.percentages,
            payment.totalAmount,
            payment.collectedAmount,
            payment.isActive,
            payment.creator
        );
    }
    
    // Check contribution amount
    function getContribution(uint256 _paymentId, address _contributor) 
        public view returns (uint256) {
        return contributions[_paymentId][_contributor];
    }
}
