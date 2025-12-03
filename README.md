# CRM System - Deployment Guide für PythonAnywhere
### 1. Lokales Setup (Windows)

```bash
git clone https://github.com/kelias-gh/CRM.git CRM_EKlein

cd CRM_EKlein

pip install -r requirements.txt

python setup_database.py

python app.py
```

### 2. PythonAnywhere Deployment

#### Python Venv erstellen & Files hochladen
1. Log in [PythonAnywhere](https://www.pythonanywhere.com/)
2. Bash öffnen (Consoles Tab)
```bash
git clone https://github.com/kelias-gh/CRM.git CRM_EKlein

cd CRM_EKlein

python -m venv ./

pip install -r requirements.txt

python setup_database.py 
```

#### Web App konfigurieren
1. Zum "Web" Tab
2. Klicke "New Web App"
3. Wähle "Flask" + Python 3.12
4. Source/Working Directory: ```/home/username/CRM_EKlein```
5. Im WSGI config file (Web -> Runterscrollen "Code" -> WSGI Configuration file) und das folgende einfügen:

```python
import sys
sys.path.insert(0, './')

from app import create_app
application = create_app()
```

#### Web App neuladen
1. Zum "Web"
2. Grünen "Reload" button drücken
2. CRM zugreifbar bei `https://yourusername.pythonanywhere.com`

### Login 

- **Email**: `admin@crm.local`
- **Password**: `admin123`
