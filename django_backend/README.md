# Django Backend for Consultation Booking System

## Setup Instructions

### 1. Install Dependencies
```bash
cd django_backend
pip install -r requirements.txt
```

### 2. Configure Django Settings

Add to your `settings.py`:

```python
INSTALLED_APPS = [
    # ...
    'rest_framework',
    'corsheaders',
    'consultations',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    # ...
]

# CORS Settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://your-frontend-domain.com",
]

CORS_ALLOW_CREDENTIALS = True

# Email Configuration (Use Gmail SMTP or SendGrid)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'Agency.io <your-email@gmail.com>'
ADMIN_EMAIL = 'admin@agency.io'
SITE_URL = 'http://localhost:8000'

# REST Framework Settings
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}
```

### 3. Update URLs

In your main `urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('consultations.urls')),
]
```

### 4. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser
```bash
python manage.py createsuperuser
```

### 6. Run Development Server
```bash
python manage.py runserver
```

## API Endpoints

### List/Create Consultations
- **GET** `/api/consultations/` - List all consultations
- **POST** `/api/consultations/` - Create new consultation

### Retrieve/Update/Delete Consultation
- **GET** `/api/consultations/{id}/` - Get consultation details
- **PUT** `/api/consultations/{id}/` - Update consultation
- **DELETE** `/api/consultations/{id}/` - Delete consultation

### Custom Actions
- **POST** `/api/consultations/{id}/confirm/` - Confirm booking
- **POST** `/api/consultations/{id}/cancel/` - Cancel booking

## Frontend Integration

1. Update `DJANGO_API_URL` in `booking.js`:
```javascript
const DJANGO_API_URL = 'http://localhost:8000/api';
```

2. Include the booking modal and script in your HTML:
```html
<!-- Before closing </body> tag -->
<script src="booking.js"></script>
```

3. Load the booking modal HTML (use AJAX or include directly)

## Email Setup (Gmail)

1. Enable 2-Factor Authentication on Gmail
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Use app password in `EMAIL_HOST_PASSWORD`

## Production Deployment

1. Set `DEBUG = False`
2. Configure proper database (PostgreSQL recommended)
3. Set up static files serving
4. Use environment variables for sensitive data
5. Configure HTTPS
6. Set proper CORS origins

## Admin Panel

Access at: `http://localhost:8000/admin/`

### Features:
- View all consultation bookings
- Filter by status, project type, date
- Search by name, email, company
- Bulk actions (confirm, complete, cancel)
- Add internal notes

## Testing

```bash
python manage.py test consultations
```