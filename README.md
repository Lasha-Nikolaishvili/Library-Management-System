# Library Management System

## Introduction

The Library Management System is a Django-based web application designed to manage library operations such as book reservations, checkouts, and returns. It includes features for tracking book inventory, managing user accounts, and generating various statistics.

## Features

- Web scraped data of more than 1000 books
- User registration and authentication
- Book reservation and checkout
- Automatic notifications for overdue books
- Automatic cancellation of overdue reservations
- Detailed statistics on book usage and user activity
- Customized Admin interface for managing books, authors, genres, and users
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

   The project comes with a sqlite3 database by default. You can see the admin user credentials near the end of file.

5. **Configure the email server**
    
   The application sends email notifications for overdue books. You can configure the email server settings in the `.env` file:
   
   ```sh
   EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
   EMAIL_HOST = 'smtp.gmail.com'
   EMAIL_PORT = 587
   EMAIL_USE_TLS = True
   EMAIL_HOST_USER = 'tbclibrarysystem1@gmail.com'
   EMAIL_HOST_PASSWORD = 'bhvlqumvmkbjllzd'
   DEFAULT_FROM_EMAIL = 'tbclibrarysystem1@gmail.com'
   ```


5. **Apply the migrations:**

    ```sh
    python manage.py migrate
    ```

6. **Collect static files:**

    ```sh
    python manage.py collectstatic
    ```

7. **Run the development server:**

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

### Reserving Books

Users can browse available books and make reservations through the main interface. The system will check for book availability and ensure users do not reserve more than one book at a time.

### Overdue Notifications

A management command is available to send email notifications to users with overdue checkouts:

```sh
python manage.py send_overdue_checkout_email
```

This command can be scheduled to run periodically using a task scheduler like `cron`.


### Rest API

The application provides a REST API to interact with the library system programmatically:

- List all books, authors, genres, customers, checkouts and reservations with pagination
- Retrieve, create, update, and delete individual records
- Search and filter records by different fields
- Customers can reserve books

Endpoints are available under the `/rest-api/` URL.

### Statistics API

The application provides a statistics API to generate various reports:

- Most popular books
- Checkout counts for the past year
- Top books returned late
- Top customers who returned books late

Endpoints are available under the `/statistics/` URL.

## Admin User Credentials

- Email: admin@mail.com
- Password: admin

## Technologies And Apps Used

- Django
- Django REST Framework
- markdown
- Swagger UI
- Debug Toolbar
- Admin Auto Filters
- Django Filters
- Python Decouple
- Bootstrap
- Font Awesome

## Authors

- [Lasha-Nikolaishvili](https://github.com/Lasha-Nikolaishvili)
