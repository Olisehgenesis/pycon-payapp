# Payment Splitter Flask App 🚀

A beautiful web interface for the Payment Splitter DApp built with Flask and Web3.

## Features ✨

- **Modern UI/UX** - Beautiful, responsive design with Bootstrap 5
- **Real-time Updates** - Live payment data from the blockchain
- **Interactive Forms** - Dynamic recipient management with validation
- **Payment Tracking** - Visual progress bars and statistics
- **Mobile Responsive** - Works perfectly on all devices
- **Blockchain Integration** - Direct connection to Celo Alfajores

## Quick Start 🚀

### 1. Setup Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment
Create a `.env` file in the project root:
```bash
# Contract Configuration
CONTRACT_ADDRESS=0x0175dDbE48ea455bbFE21E6E36a4f59781f90BE9

# Flask Configuration
SECRET_KEY=your-secret-key-change-this-in-production
FLASK_ENV=development
FLASK_DEBUG=1

# Celo Network Configuration
CELO_RPC_URL=https://alfajores-forno.celo-testnet.org
EXPLORER_URL=https://alfajores.celoscan.io
```

### 3. Run the App
```bash
python app.py
```

The app will be available at: http://localhost:5000

## Project Structure 📁

```
pycon-app/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables
├── templates/            # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Dashboard page
│   ├── create_payment.html # Create payment form
│   ├── pay_invoice.html  # Pay invoice form
│   └── view_payment.html # Payment details page
├── static/               # Static assets
│   ├── css/
│   │   └── style.css     # Custom CSS styles
│   └── js/
│       └── app.js        # JavaScript functionality
└── README.md            # This file
```

## Pages & Features 🎯

### Dashboard (`/`)
- **Payment Statistics** - Total payments, active payments, CELO managed
- **Recent Payments** - Live feed of all payments with progress
- **Quick Actions** - Create payment and pay invoice buttons
- **Features Section** - Why use Payment Splitter

### Create Payment (`/create_payment`)
- **Dynamic Forms** - Add/remove recipients with real-time validation
- **Percentage Calculator** - Automatic total calculation
- **Address Validation** - Ethereum address format checking
- **Help Section** - Step-by-step instructions

### Pay Invoice (`/pay_invoice`)
- **Payment ID Input** - Enter payment ID to contribute
- **Amount Input** - Specify contribution amount
- **Recent Payments** - Quick access to active payments
- **Form Validation** - Ensures valid inputs

### View Payment (`/view_payment/<id>`)
- **Payment Details** - Complete payment information
- **Progress Tracking** - Visual progress bars and statistics
- **Recipient List** - All recipients with their shares
- **Action Buttons** - Pay invoice, copy payment ID

## API Endpoints 🔌

### GET `/api/payments`
Returns all payments as JSON:
```json
[
  {
    "id": 0,
    "description": "Dinner at Cafe Javas",
    "total_amount": 0.05,
    "collected_amount": 0.02,
    "is_active": true,
    "progress": 40.0
  }
]
```

## Technologies Used 🛠️

- **Backend**: Flask (Python)
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Blockchain**: Web3.py, Celo Alfajores
- **Styling**: Custom CSS with animations
- **Icons**: Font Awesome 6
- **Fonts**: Google Fonts (Inter)

## Design Features 🎨

### Modern UI/UX
- **Gradient Backgrounds** - Beautiful color schemes
- **Card-based Layout** - Clean, organized information
- **Hover Effects** - Interactive elements with smooth transitions
- **Progress Bars** - Visual payment progress tracking
- **Responsive Design** - Works on all screen sizes

### Animations
- **Fade-in Effects** - Smooth page loading
- **Slide Animations** - Dynamic form elements
- **Loading States** - User feedback during operations
- **Smooth Transitions** - Professional feel

### Interactive Elements
- **Real-time Validation** - Form validation as you type
- **Dynamic Forms** - Add/remove recipients
- **Copy to Clipboard** - Easy payment ID sharing
- **Auto-refresh** - Live data updates

## Configuration ⚙️

### Environment Variables
- `CONTRACT_ADDRESS` - Deployed contract address
- `SECRET_KEY` - Flask secret key
- `CELO_RPC_URL` - Celo network RPC endpoint
- `EXPLORER_URL` - Blockchain explorer URL

### Customization
- **Colors**: Modify CSS variables in `static/css/style.css`
- **Icons**: Replace Font Awesome icons
- **Layout**: Adjust Bootstrap classes in templates
- **Functionality**: Extend JavaScript in `static/js/app.js`

## Development 🛠️

### Adding New Features
1. **Backend**: Add routes in `app.py`
2. **Frontend**: Create templates in `templates/`
3. **Styling**: Add CSS in `static/css/style.css`
4. **Interactivity**: Add JavaScript in `static/js/app.js`

### Testing
```bash
# Run with debug mode
FLASK_DEBUG=1 python app.py

# Access at http://localhost:5000
```

## Deployment 🚀

### Production Setup
1. **Environment**: Set `FLASK_ENV=production`
2. **Secret Key**: Generate secure secret key
3. **HTTPS**: Use SSL certificate
4. **Database**: Add database for user management
5. **Wallet Integration**: Add MetaMask/Valora integration

### Docker (Optional)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

## Contributing 🤝

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## License 📄

MIT License - see LICENSE file for details

---

**Built with ❤️ for the Ugandan Web3 community! 🇺🇬**

