# Online Shopping Cart

A role-based online shopping cart application built with Flask, featuring different user roles including admin, seller, and customer.

## Features

- **User Authentication**: Secure login and registration system
- **Role-Based Access Control**:
  - Admin: Manage users, products, and orders
  - Seller: Add, update, and manage products
  - Customer: Browse products, add to cart, and place orders
- **Product Management**: CRUD operations for products
- **Shopping Cart**: Add/remove items, update quantities
- **Order Processing**: Place and track orders

## Prerequisites

- Python 3.11
- pip (Python package manager)
- MySQL/PostgreSQL (or any SQL database supported by SQLAlchemy)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/jeetendra29gupta/Role-Based-Online-Shopping-Cart.git
   cd Role-Based-Online-Shopping-Cart
   ```

2. **Create and activate a virtual environment**
   ```bash
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Setup**
   - Copy `.env.example` to `.env`
   - Update the database connection string and other configurations in `.env`

5. **Initialize the database**
   ```bash
   python main.py
   ```
   This will create the necessary database tables.

## Running the Application

1. Start the development server:
   ```bash
   python main.py
   ```

2. Open your browser and visit: [http://localhost:8181](http://localhost:8181)

## Project Structure

```
PythonProject/
├── database/         # Database related files
├── docs/             # Documentation
├── logs/             # Application logs
├── src/              # Source code
│   ├── models/       # Database models
│   ├── routes/       # Application routes
│   ├── templates/    # HTML templates
│   ├── utilities/    # Helper functions and utilities
│   └── __init__.py   # Package initialization
├── static/           # Static files (CSS, JS, images)
├── templates/        # Main templates directory
├── .env              # Environment variables
├── main.py           # Application entry point
└── requirements.txt  # Project dependencies
```

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```
# Web App metadata
TITLE="Online Shopping Cart"
DESCRIPTION="Role Based Online Shopping Cart"
VERSION=1.0.0
SECRET_KEY=your-secret-key

# Flask Server
HOST=0.0.0.0
PORT=8181
DEBUG=true

# Database Configuration
DB_DRIVER=mysql+pymysql  # or postgresql+psycopg2 for PostgreSQL
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=shopping_cart

# Email Configuration (if applicable)
MAIL_SERVER=smtp.example.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@example.com
MAIL_PASSWORD=your-email-password
```

## Dependencies

- Flask - Web framework
- SQLModel - ORM and database toolkit
- Pydantic - Data validation
- python-dotenv - Environment variable management
- bcrypt - Password hashing
- email-validator - Email validation

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please open an issue in the GitHub repository.
