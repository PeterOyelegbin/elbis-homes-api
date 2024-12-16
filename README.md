# ELBIS Homes API
ELBIS Homes is a real estate platform designed to simplify the process of renting or buying properties in Nigeria. This API provides the backend infrastructure necessary for user authentication, property management, and interaction with a database of available properties.

---

## Table of Contents
* [Introduction](#introduction)
* [Features](#features)
* [Installation](#installation)
* [Usage](#usage)
* [To-Do](#to-do)
* [Acknowledgements](#acknowledgements)

---

## Introduction
The ELBIS Homes API is a Django-based server-side application that handles user authentication, property data management, and integration with a MySQL database. It is built using Python, Django Rest Framework, and JWT authentication, providing a robust and scalable foundation for real estate platforms. This project is designed for ease of use, allowing for quick integration with front-end applications or other systems.

---

## Features
- **Python Version**: 3.9
- **Python Decouple**: 3.8
- **Django Version**: 3.2
- **Django Rest Framework**: 3.15.1
- **SimpleJWT**: 5.3.1
- **Pillow**: 9.4.0
- **Cloudinary Integration**: 1.32 (for image management)
- **Database**: 
  - SQLite for local development
  - MySQL for production (via `mysqlclient` 2.1.1)
- **Basic Folder Structure**: Organized Django apps for scalability
- **JWT Authentication**: Secure token-based authentication for users
- **Property Management**: CRUD operations for properties (add, update, delete, retrieve)

---

## Installation
Before you start, ensure the following prerequisites are installed:
- **Python** (version 3.9)
- **Pip** (Python package manager)
  
### Steps to Install
1. **Clone the repository** to your local machine:
    ```bash
    git clone https://github.com/PeterOyelegbin/elbis-homes-api.git
    ```

2. **Navigate to the project directory**:
    ```bash
    cd elbis-homes-api
    ```

3. **Create a virtual environment**:
    On macOS/Linux:
    ```bash
    python3 -m venv env
    ```
    On Windows:
    ```bash
    python -m venv env
    ```

4. **Activate the virtual environment**:
    On macOS/Linux:
    ```bash
    source env/bin/activate
    ```
    On Windows:
    ```bash
    env\Scripts\activate
    ```

5. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

6. **Run database migrations** to set up the SQLite database:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

7. **Start the development server**:
    ```bash
    python manage.py runserver
    ```

8. Open your web browser and navigate to `http://127.0.0.1:8000/` to see the Django API view page.

---

## To-Do
Future enhancements are planned for this API:
- **Favorites**: Enable users to save favorite properties.
- **Reviews**: Allow users to leave reviews for properties.
- **Search and Filters**: Advanced search and filtering options based on property type, price range, location, etc.

Additional features will be added in subsequent versions.

---

## Acknowledgements
Special thanks to **[Frontend dev](https://philipoyelegbin.github.io)** for integrating this API with a React frontend, creating a fully functional real estate application.
