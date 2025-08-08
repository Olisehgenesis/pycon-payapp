// Payment Splitter DApp - JavaScript

// Global variables
let currentRecipientCount = 0;
let web3 = null;
let userAccount = null;

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Add fade-in animation to cards
    addFadeInAnimation();
    
    // Initialize tooltips
    initializeTooltips();
    
    // Add smooth scrolling
    addSmoothScrolling();
    
    // Initialize form validation
    initializeFormValidation();
    
    // Initialize MetaMask connection
    initializeMetaMask();
}

// Add fade-in animation to elements
function addFadeInAnimation() {
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'opacity 0.5s ease-in-out, transform 0.5s ease-in-out';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
}

// Initialize Bootstrap tooltips
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Add smooth scrolling
function addSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Form validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
}

// Add recipient to payment form
function addRecipient() {
    const recipientsContainer = document.getElementById('recipients-container');
    const recipientTemplate = `
        <div class="recipient-item mb-3" id="recipient-${currentRecipientCount}">
            <div class="row">
                <div class="col-md-6 mb-2">
                    <label class="form-label">Recipient Address</label>
                    <input type="text" class="form-control" name="recipients[]" 
                           placeholder="0x..." required 
                           pattern="^0x[a-fA-F0-9]{40}$">
                    <div class="invalid-feedback">
                        Please enter a valid Ethereum address
                    </div>
                </div>
                <div class="col-md-4 mb-2">
                    <label class="form-label">Percentage</label>
                    <input type="number" class="form-control percentage-input" 
                           name="percentages[]" min="1" max="100" required>
                    <div class="invalid-feedback">
                        Please enter a percentage between 1-100
                    </div>
                </div>
                <div class="col-md-2 mb-2 d-flex align-items-end">
                    <button type="button" class="btn btn-outline-danger btn-sm" 
                            onclick="removeRecipient(${currentRecipientCount})">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        </div>
    `;
    
    recipientsContainer.insertAdjacentHTML('beforeend', recipientTemplate);
    currentRecipientCount++;
    
    // Add slide-in animation
    const newRecipient = document.getElementById(`recipient-${currentRecipientCount - 1}`);
    newRecipient.style.opacity = '0';
    newRecipient.style.transform = 'translateX(-100%)';
    
    setTimeout(() => {
        newRecipient.style.transition = 'opacity 0.3s ease-out, transform 0.3s ease-out';
        newRecipient.style.opacity = '1';
        newRecipient.style.transform = 'translateX(0)';
    }, 10);
}

// Remove recipient from payment form
function removeRecipient(index) {
    const recipient = document.getElementById(`recipient-${index}`);
    if (recipient) {
        recipient.style.transition = 'opacity 0.3s ease-out, transform 0.3s ease-out';
        recipient.style.opacity = '0';
        recipient.style.transform = 'translateX(-100%)';
        
        setTimeout(() => {
            recipient.remove();
        }, 300);
    }
}

// Calculate total percentage
function calculateTotalPercentage() {
    const percentageInputs = document.querySelectorAll('.percentage-input');
    let total = 0;
    
    percentageInputs.forEach(input => {
        const value = parseInt(input.value) || 0;
        total += value;
    });
    
    const totalDisplay = document.getElementById('total-percentage');
    if (totalDisplay) {
        totalDisplay.textContent = total;
        totalDisplay.className = total === 100 ? 'text-success' : 'text-danger';
    }
    
    return total;
}

// Format CELO amount
function formatCelo(amount) {
    return parseFloat(amount).toFixed(4) + ' CELO';
}

// Format address for display
function formatAddress(address) {
    if (!address) return '';
    return address.substring(0, 6) + '...' + address.substring(address.length - 4);
}

// Show loading state
function showLoading(element) {
    element.classList.add('loading');
    element.disabled = true;
}

// Hide loading state
function hideLoading(element) {
    element.classList.remove('loading');
    element.disabled = false;
}

// Show success message
function showSuccess(message) {
    showAlert(message, 'success');
}

// Show error message
function showError(message) {
    showAlert(message, 'danger');
}

// Show alert message
function showAlert(message, type) {
    const alertContainer = document.createElement('div');
    alertContainer.className = `alert alert-${type} alert-dismissible fade show`;
    alertContainer.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-triangle'} me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    container.insertBefore(alertContainer, container.firstChild);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        if (alertContainer.parentNode) {
            alertContainer.remove();
        }
    }, 5000);
}

// Copy to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showSuccess('Copied to clipboard!');
    }).catch(() => {
        showError('Failed to copy to clipboard');
    });
}

// Refresh payments data
function refreshPayments() {
    fetch('/api/payments')
        .then(response => response.json())
        .then(data => {
            if (typeof updatePaymentsList === 'function') {
                updatePaymentsList(data);
            }
            if (typeof updateStats === 'function') {
                updateStats(data);
            }
        })
        .catch(error => {
            console.error('Error refreshing payments:', error);
        });
}

// Auto-refresh every 30 seconds
setInterval(refreshPayments, 30000);

// Add event listeners for percentage inputs
document.addEventListener('input', function(e) {
    if (e.target.classList.contains('percentage-input')) {
        calculateTotalPercentage();
    }
});

// Add event listeners for address validation
document.addEventListener('input', function(e) {
    if (e.target.name === 'recipients[]') {
        validateAddress(e.target);
    }
});

// Validate Ethereum address
function validateAddress(input) {
    const address = input.value;
    const isValid = /^0x[a-fA-F0-9]{40}$/.test(address);
    
    if (address && !isValid) {
        input.classList.add('is-invalid');
    } else {
        input.classList.remove('is-invalid');
    }
}

// Initialize payment form
function initializePaymentForm() {
    // Add first recipient by default
    addRecipient();
    
    // Add event listener for add recipient button
    const addButton = document.getElementById('add-recipient-btn');
    if (addButton) {
        addButton.addEventListener('click', addRecipient);
    }
}

// Initialize when payment form is loaded
if (document.getElementById('recipients-container')) {
    initializePaymentForm();
}

// Handle form submissions with MetaMask
function initializeFormHandlers() {
    // Create payment form handler
    const createPaymentForm = document.getElementById('create-payment-form');
    if (createPaymentForm) {
        createPaymentForm.addEventListener('submit', handleCreatePayment);
    }
    
    // Pay invoice form handler
    const payInvoiceForm = document.getElementById('pay-invoice-form');
    if (payInvoiceForm) {
        payInvoiceForm.addEventListener('submit', handlePayInvoice);
    }
}

async function handleCreatePayment(event) {
    event.preventDefault();
    
    if (!userAccount) {
        showError('Please connect your wallet first');
        return;
    }
    
    const formData = new FormData(event.target);
    
    try {
        showLoading(event.target);
        
        const response = await fetch('/create_payment', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            const txHash = await sendTransaction(result.tx_data);
            if (txHash) {
                event.target.reset();
                window.location.href = '/';
            }
        } else {
            showError(result.error || 'Failed to create payment');
        }
    } catch (error) {
        console.error('Error:', error);
        showError('Failed to create payment');
    } finally {
        hideLoading(event.target);
    }
}

async function handlePayInvoice(event) {
    event.preventDefault();
    
    if (!userAccount) {
        showError('Please connect your wallet first');
        return;
    }
    
    const formData = new FormData(event.target);
    
    try {
        showLoading(event.target);
        
        const response = await fetch('/pay_invoice', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            const txHash = await sendTransaction(result.tx_data);
            if (txHash) {
                event.target.reset();
                window.location.href = '/';
            }
        } else {
            showError(result.error || 'Failed to pay invoice');
        }
    } catch (error) {
        console.error('Error:', error);
        showError('Failed to pay invoice');
    } finally {
        hideLoading(event.target);
    }
}

// Initialize form handlers when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeFormHandlers();
});

// MetaMask Integration
function initializeMetaMask() {
    // Check if MetaMask is installed
    if (typeof window.ethereum !== 'undefined') {
        web3 = new Web3(window.ethereum);
        console.log('MetaMask is installed!');
        
        // Add connect button to the page
        addConnectButton();
        
        // Listen for account changes
        window.ethereum.on('accountsChanged', function (accounts) {
            if (accounts.length === 0) {
                userAccount = null;
                updateConnectButton();
            } else {
                userAccount = accounts[0];
                updateConnectButton();
            }
        });
        
        // Check if already connected
        window.ethereum.request({ method: 'eth_accounts' })
            .then(accounts => {
                if (accounts.length > 0) {
                    userAccount = accounts[0];
                    updateConnectButton();
                }
            });
    } else {
        console.log('MetaMask is not installed');
        showError('Please install MetaMask to use this app');
    }
}

function addConnectButton() {
    const navbar = document.querySelector('.navbar-nav');
    if (navbar && !document.getElementById('connect-btn')) {
        const connectBtn = document.createElement('li');
        connectBtn.className = 'nav-item';
        connectBtn.innerHTML = `
            <button id="connect-btn" class="btn btn-outline-light btn-sm">
                <i class="fas fa-wallet me-1"></i>
                Connect Wallet
            </button>
        `;
        navbar.appendChild(connectBtn);
        
        document.getElementById('connect-btn').addEventListener('click', connectMetaMask);
    }
}

function updateConnectButton() {
    const connectBtn = document.getElementById('connect-btn');
    if (connectBtn) {
        if (userAccount) {
            connectBtn.innerHTML = `
                <i class="fas fa-wallet me-1"></i>
                ${userAccount.slice(0, 6)}...${userAccount.slice(-4)}
            `;
            connectBtn.className = 'btn btn-success btn-sm';
        } else {
            connectBtn.innerHTML = `
                <i class="fas fa-wallet me-1"></i>
                Connect Wallet
            `;
            connectBtn.className = 'btn btn-outline-light btn-sm';
        }
    }
}

async function connectMetaMask() {
    if (typeof window.ethereum !== 'undefined') {
        try {
            // Request account access
            const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
            userAccount = accounts[0];
            updateConnectButton();
            showSuccess('Wallet connected successfully!');
        } catch (error) {
            console.error('Error connecting to MetaMask:', error);
            showError('Failed to connect wallet');
        }
    } else {
        showError('Please install MetaMask');
    }
}

async function sendTransaction(txData) {
    if (!userAccount) {
        showError('Please connect your wallet first');
        return null;
    }
    
    try {
        // Get the current network
        const chainId = await window.ethereum.request({ method: 'eth_chainId' });
        
        // Check if we're on Celo Alfajores (chainId: 0xaef3)
        if (chainId !== '0xaef3') {
            showError('Please switch to Celo Alfajores testnet');
            return null;
        }
        
        // Get the nonce
        const nonce = await web3.eth.getTransactionCount(userAccount, 'pending');
        
        // Prepare transaction
        const transaction = {
            from: userAccount,
            to: txData.to,
            data: txData.data,
            gas: txData.gas,
            gasPrice: txData.gasPrice,
            nonce: nonce
        };
        
        if (txData.value) {
            transaction.value = txData.value;
        }
        
        // Send transaction
        const txHash = await window.ethereum.request({
            method: 'eth_sendTransaction',
            params: [transaction]
        });
        
        showSuccess(`Transaction sent! Hash: ${txHash}`);
        return txHash;
        
    } catch (error) {
        console.error('Transaction error:', error);
        showError('Transaction failed: ' + error.message);
        return null;
    }
}

