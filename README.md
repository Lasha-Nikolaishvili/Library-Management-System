# Library Management System

## Introduction

The Library Management System is a Django-based web application designed to manage library operations such as book reservations, checkouts, and returns. It includes features for tracking book inventory, managing user accounts, and generating various statistics.

## Features

- User registration and authentication
- Book reservation and checkout
- Automatic notifications for overdue books
- Detailed statistics on book usage and user activity
- Admin interface for managing books, authors, genres, and users
- User interface for browsing books and making reservations

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/Lasha-Nikolaishvili/Library-Management-System.git
    cd library-management-system
    ```

2. **Create a virtual environment:**

    ```sh
    python -m venv venv
    source venv/bin/activate
    ```

3. **Install the dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Configure the database:**

    Modify the `DATABASES` setting in `library_management_system/settings.py` to match your database configuration.

5. **Apply the migrations:**

    ```sh
    python manage.py migrate
    ```

6. **Create a superuser:**

    ```sh
    python manage.py createsuperuser
    ```

7. **Collect static files:**

    ```sh
    python manage.py collectstatic
    ```

8. **Run the development server:**

    ```sh
    python manage.py runserver
    ```

## Usage

### Admin Interface

Access the admin interface at `http://localhost:8000/admin` to manage books, authors, genres, and users. Use the credentials created during the superuser creation step.

### User Registration and Login

Users can register and log in via the following URLs:

- Register: `http://localhost:8000/register`
- Login: `http://localhost:8000/login`

### Reserving and Checking Out Books

Users can browse available books and make reservations through the main interface. The system will check for book availability and ensure users do not reserve more than one book at a time.

### Overdue Notifications

A management command is available to send email notifications to users with overdue checkouts:

```sh
python manage.py send_overdue_notifications
```

This command can be scheduled to run periodically using a task scheduler like `cron` or a Django task scheduling package like `django-celery-beat`.

### Statistics API

The application provides a statistics API to generate various reports:

- Most popular books
- Checkout counts for the past year
- Top books returned late
- Top customers who returned books late

Endpoints are available under the `/statistics/` URL.

## Customization

### Email Settings

Configure email settings in `settings.py` to enable email notifications:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'your_smtp_server'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@example.com'
EMAIL_HOST_PASSWORD = 'your_email_password'
DEFAULT_FROM_EMAIL = 'your_email@example.com'
```

### Static and Media Files

Configure the `STATIC_URL` and `MEDIA_URL` settings in `settings.py` to serve static and media files correctly:

```python
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'library/static')]
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes. Ensure that your code follows the project's coding standards and includes appropriate tests.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

This README provides a comprehensive overview of the Library Management System, covering installation, usage, customization, and contribution guidelines.