# Django User Registration and Task Management

This Django web application allows users to register, verify their accounts with OTP, and manage tasks seamlessly. The software provides real-time feedback during registration, OTP verification, and task management. It uses a PostgreSQL database for data storage and offers a smooth user experience.

## Table of Contents

1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Technologies Used](#technologies-used)
6. [License](#license)

## Features

1. **User Registration**
   - Users must register with a unique username, email, and matching passwords.
   - Real-time feedback during registration:
     - Availability check for username and email.
     - Password and confirm password matching check.

2. **Account Verification**
   - After registration, a verification OTP is sent to the registered email.
   - User accounts are marked as not verified until OTP validation.
   - OTP validation is mandatory during login.
   - OTPs are valid for one hour since generation.
   - Users can generate a new OTP and receive it via email.

3. **Task Management**
   - Users can:
     - Add tasks.
     - Update tasks.
     - Delete tasks.
     - Mark tasks as completed.
   - Completed tasks can be viewed on a separate page.

4. **Logout Option**
   - Users can log out from the index page.

5. **Smooth User Experience**
   - The application is designed to provide a smooth and responsive user interface.

6. **Database**
   - PostgreSQL is used as the database for data storage.

## Prerequisites

Before setting up and running the application, ensure you have the following prerequisites installed:

- Python (3.7+)
- Django
- PostgreSQL
- SMTP server for sending verification OTP emails
- Other dependencies (specified in `requirements.txt`)

## Installation

1. Clone the repository to your local machine:

   ```shell
   git clone <repository-url>
   ```

2. Install the required dependencies:

   ```shell
   pip install -r requirements.txt
   ```

3. Configure your PostgreSQL database settings in `settings.py`:

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'your_database_name',
           'USER': 'your_database_user',
           'PASSWORD': 'your_database_password',
           'HOST': 'localhost',  # Update if your database is hosted elsewhere
           'PORT': '5432',       # Update if your database uses a different port
       }
   }
   ```

4. Apply database migrations:

   ```shell
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Run the development server:

   ```shell
   python manage.py runserver
   ```

## Usage

1. Access the application in your web browser at `http://localhost:8000/`.

2. Register a new account with a unique username, email, and matching passwords.

3. Verify your account by entering the OTP sent to your registered email.

4. Log in and start managing your tasks.

## Technologies Used

- Python
- Django
- PostgreSQL
- HTML/CSS
- JavaScript
- SMTP (for sending OTP emails)

