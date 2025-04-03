# P1X3L - File Sharing Application

A django project for image sharing.
Like imgur.

## Features

- User authentication and authorization
- File upload and management
- Public and private file sharing
- User profiles
- Secure file serving
- Environment-based configuration

## Prerequisites

- Python 3.x
- Django 5.1.7
- SQLite3 (default database)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd p1x3l
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Configure the following variables in `.env`:
     - `SECRET_KEY`: Django secret key
     - `DEBUG`: Debug mode (True/False)
     - `PASSWORD_SALT`: Salt for password hashing

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

## Running the Application

1. Start the development server:
```bash
python manage.py runserver
```

2. Access the application at `http://localhost:8000`

## Project Structure

- `app/`: Main application directory
  - `views.py`: View functions and routes
  - `models.py`: Database models
  - `services/`: Business logic services
- `p1x3l/`: Project configuration
  - `settings.py`: Django settings
  - `urls.py`: URL routing
- `user_content/`: Directory for uploaded files
- `manage.py`: Django management script

## Features in Detail

- **User Management**
  - Registration and login
  - User profiles
  - Authentication state management

- **File Management**
  - File upload
  - Public/private file visibility toggle
  - File deletion
  - Secure file serving

- **Security**
  - Environment-based configuration
  - Password salting
  - Login required decorators
  - Secure file handling