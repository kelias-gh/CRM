# Simple CRM System

A lightweight Customer Relationship Management system built with Flask, designed for educational purposes and small business use.

## Features

- **Customer Management**: Track customer information, contact details, and interaction history
- **Order Management**: Manage customer orders with status tracking and revenue calculations
- **Contact Logging**: Record all customer interactions (phone, email, meetings, chat)
- **KPI Dashboard**: Visualize customer revenue, activity metrics, and performance indicators
- **Search & Filter**: Find customers, orders, and contacts quickly
- **Responsive Design**: Works on desktop and mobile devices

## Technology Stack

- **Backend**: Flask (Python web framework)
- **Database**: SQLite (easily portable to MySQL/PostgreSQL)
- **Frontend**: Bootstrap 5, Jinja2 templates
- **Authentication**: Flask-Login
- **Database ORM**: SQLAlchemy

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd crm-system

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Setup

```bash
# Initialize database with sample data
python setup_database.py
```

### 3. Run the Application

```bash
# Start the development server
python app.py

# Or use Flask command
flask run
```

### 4. Access the Application

Open your browser and go to: `http://localhost:5000`

**Default Login:**
- Email: `admin@crm.local`
- Password: `admin123`

## Database Schema

The system uses the following database tables:

- **customers**: Customer information
- **orders**: Customer orders with status and amounts
- **order_items**: Individual items within orders
- **products**: Product catalog
- **contacts**: Customer interaction history
- **users**: System users with authentication

## File Structure

```
crm-system/
├── app.py              # Main Flask application
├── models.py           # Database models
├── config.py           # Configuration settings
├── setup_database.py   # Database initialization script
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates
│   ├── base.html      # Base template
│   ├── index.html     # Dashboard
│   ├── login.html     # Login page
│   └── customer_detail.html  # Customer details
└── DEPLOYMENT_GUIDE.md # Deployment instructions
```

## Configuration

Environment variables can be set in `.env` file:

```env
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///crm.db
FLASK_ENV=development
```

## Deployment

For production deployment, see [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions on:
- PythonAnywhere deployment
- Production configuration
- Security considerations
- Troubleshooting

## Customization

### Adding New Features

1. **Database**: Add new models in `models.py`
2. **Routes**: Add new routes in `app.py`
3. **Templates**: Create new HTML templates in `templates/`
4. **Static Files**: Add CSS/JS files and update templates

### Styling

The application uses Bootstrap 5. Custom styles can be added to:
- `templates/base.html` (global styles)
- Individual templates (page-specific styles)

## Development

### Running Tests
```bash
# Install development dependencies
pip install pytest

# Run tests
pytest
```

### Database Migrations
```bash
# Initialize migration repository
flask db init

# Create migration
flask db migrate -m "Description"

# Apply migration
flask db upgrade
```

## Educational Use

This CRM system is designed for educational purposes and includes:
- Clean, documented code
- Common web development patterns
- Database design best practices
- User authentication
- Responsive web design

Students can learn:
- Flask web development
- SQLAlchemy ORM
- Database design
- Frontend/backend integration
- Deployment practices

## License

This project is open source and available under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For questions or issues:
1. Check the deployment guide
2. Review the code documentation
3. Check existing issues
4. Create a new issue with detailed description