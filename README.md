## Flight Application Overview

### Project Description

Our flight application is a comprehensive platform designed to manage and search flights efficiently. While administrators have the ability to add new flights, users can only search for existing flights based on various filters.

### Key Features

1. **Flight Management**:
    - **Administrator Flight Addition**: Only administrators can add new flights to the system. They can input details such as flight number, airline, departure city, arrival city, departure schedule, arrival schedule, flight duration, and available seats.
    - **User Flight Search**: Users can search for flights using filters like date, time, airline, and more to find flights that meet their specific needs.
2. **User Registration and Authentication**:
    - **User Registration**: Users can create an account within the system.
    - **Token-Based Authentication**: Upon login, users receive a secure authentication token that must be included in API requests, ensuring that only authenticated users can access certain features.
    - **Hashed Password Storage**: To enhance security, user passwords are hashed before being stored in the database.
3. **Asynchronous Tasks**:
    - **Email Notifications**: Celery, an asynchronous task queue, along with SMTP, is used to handle tasks such as sending email notifications. Users are informed of any changes to flight details via email.
    - **Scheduled Notifications**: Celery Beat is used to schedule periodic notifications, ensuring timely updates and reminders related to flights.
4. **Logging Service**:
    - **Comprehensive Logging**: The application includes a robust logging service to monitor and debug operations. It logs various activities, including errors, warnings, and informational messages, to ensure smooth operation and quick resolution of issues.

### Technology Stack

- **Backend**: Python
- **Database**: PostgreSQL
- **Frontend**: React
- **Asynchronous Task Management**: Celery
- **Email Notifications**: SMTP
- **Scheduled Tasks**: Celery Beat
- **Logging**: Custom logging service

### Security and Authentication

- **Token-Based API Authentication**: All API endpoints are secured and require a valid authentication token for access.
- **Password Hashing**: User passwords are hashed using a secure algorithm before storage to ensure data protection.

### Summary

This flight application offers a robust platform for flight management and search functionalities. While only administrators can add flights, users benefit from secure, token-based access and efficient notification of flight changes through asynchronous tasks. The application is designed to provide a smooth and secure experience for both administrators and users, with scheduled notifications and comprehensive logging to ensure reliable operation.
