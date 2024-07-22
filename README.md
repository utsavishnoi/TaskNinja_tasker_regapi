# TaskNinja Tasker API

## Overview
TaskNinja API provides RESTful endpoints for user authentication and task management. It allows users to register, log in, and manage tasks.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [URLs](#urls)
  - [Auth App](#auth-app)
  - [Token Management](#token-management)
  - [Request Management](#request-management)
- [Notes](#notes)

## Installation

1. Clone the repository:
    ```sh
    git clone [https://github.com/your-repo/django-project.git](https://github.com/utsavishnoi/TaskNinja_tasker_regapi)
    cd backend
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Apply migrations:
    ```sh
    python manage.py migrate
    ```

4. Create a superuser to access the Django admin:
    ```sh
    python manage.py createsuperuser
    ```

5. Run the development server:
    ```sh
    python manage.py runserver
    ```

## Usage

- Access the Django admin at `http://localhost:8000/admin/`
- Register users and taskers
- Manage addresses and requests

## URLs

### Auth App and User Management

```plaintext
- /home/ : Home view
- /user/register/ : User registration
- /tasker/register/ : Tasker registration
- /taskers/<str:service_name>/<int:address_id> : List taskers by service
- /tasker/data/ : Tasker data
- /user/data/ : User data
- /tasker/data/delete/<int:user_id> : Delete tasker data
- /tasker/update/<int:user_id> : Update tasker data
- /api/addresses/update/<str:id>/ : Update address
- /api/addresses/delete/<str:id>/ : Delete address
- /users/<str:username>/addresses/ : Create address
- /otp/ : Send OTP
- /send_password_reset_otp/ : Send password reset OTP
- /reset_password_with_otp/ : Reset password with OTP
```
### Token Management
```plaintext
- /admin/ : Django admin
- /api/token/ : Obtain JWT token
- /api/token/refresh/ : Refresh JWT token
- /api-auth/ : DRF login
``` 
### Request Management
```plaintext
- /user/request/ : Send request
- /requests/ : List requests
- /cancel/<int:req_id> : Cancel request
- /tasker/reject/<int:req_id> : Tasker reject request
- /tasker/accept/<int:req_id> : Tasker accept request
- /requests/history/ : Request history
```
