# CRM System - Deployment Guide

## Quick Setup for PythonAnywhere

### 1. Local Development Setup

```bash
# Clone or upload the files to your local machine
cd /path/to/crm-project

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup database
python setup_database.py

# Run locally
python app.py
```

### 2. PythonAnywhere Deployment

#### Step 1: Upload Files
1. Log in to [PythonAnywhere](https://www.pythonanywhere.com/)
2. Go to "Files" tab
3. Upload all files to your home directory:
   - `app.py`
   - `models.py`
   - `config.py`
   - `requirements.txt`
   - `setup_database.py`
   - The entire `templates/` directory

#### Step 2: Create Virtual Environment
1. Go to "Consoles" tab
2. Start a new Bash console
3. Run:
```bash
mkvirtualenv --python=/usr/bin/python3.9 crm-env
pip install -r requirements.txt
```

#### Step 3: Setup Database
```bash
# In the same bash console
python setup_database.py
```

#### Step 4: Configure Web App
1. Go to "Web" tab
2. Click "Add a new web app"
3. Choose "Flask" and select Python 3.9
4. For the project path, use: `/home/yourusername/crm-env`
5. In the WSGI configuration file, replace with:

```python
import sys
sys.path.insert(0, '/home/yourusername')

from app import create_app
application = create_app()
```

#### Step 5: Static Files Mapping
1. In the Web tab, scroll to "Static files"
2. Add URL: `/static/` → Directory: `/home/yourusername/static`

#### Step 6: Reload Web App
1. Click the green "Reload" button
2. Your CRM should be accessible at: `https://yourusername.pythonanywhere.com`

### 3. Default Login Credentials

- **Email**: `admin@crm.local`
- **Password**: `admin123`

### 4. Database Management

#### Backup Database
```bash
# Download the database file
# For SQLite: /home/yourusername/crm.db
```

#### Reset Database
```bash
# In PythonAnywhere Bash console
workon crm-env
python setup_database.py
```

### 5. Environment Variables (Optional)

For production, set these in PythonAnywhere:
1. Go to "Web" tab → "WSGI configuration file"
2. Add environment variables:
```python
import os
os.environ['SECRET_KEY'] = 'your-production-secret-key'
os.environ['FLASK_ENV'] = 'production'
```

### 6. Troubleshooting

#### Common Issues:
1. **Database locked**: Restart the web app
2. **Module not found**: Ensure virtual environment is activated
3. **Permission errors**: Check file permissions in PythonAnywhere files tab

#### Debug Mode:
For debugging, temporarily enable debug mode in `config.py`:
```python
DEBUG = True
```

### 7. Production Considerations

1. **Change default passwords immediately**
2. **Use environment variables for secrets**
3. **Enable HTTPS** (PythonAnywhere provides this automatically)
4. **Regular database backups**
5. **Monitor error logs** in PythonAnywhere

## Features Implemented

✅ **Customer Management**
- View all customers
- Search customers by name, email, phone
- Customer detail view with KPIs
- Contact history

✅ **Order Management**
- Global order overview (chronological)
- Order search by number or customer
- Order status tracking
- Revenue calculations

✅ **Contact Management**
- Global contact timeline
- Filter by contact channel (Phone, Email, Meeting, Chat)
- Contact history per customer

✅ **KPI Dashboard**
- Total revenue per customer
- Revenue by date range
- Last contact tracking
- Customer activity metrics

## Next Steps

1. Add customer/order/contact creation forms
2. Implement user management
3. Add reporting features
4. Export functionality
5. API endpoints for integration

## Support

For issues or questions:
1. Check PythonAnywhere error logs
2. Verify database setup
3. Ensure all dependencies are installed
4. Check file permissions