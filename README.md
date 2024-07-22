# TaskNinja Tasker API

## Overview
TaskNinja Tasker API provides RESTful endpoints for user authentication and task management. It allows users to register, log in, and manage tasks.

## Authentication APIs

### Register User
- **Endpoint**: `POST /auth/register`
- **Description**: Registers a new user.

### Login User
- **Endpoint**: `POST /auth/login`
- **Description**: Logs in an existing user.

## Task APIs

### Get All Tasks
- **Endpoint**: `GET /tasks`
- **Description**: Retrieves all tasks.

### Create Task
- **Endpoint**: `POST /tasks`
- **Description**: Creates a new task.

### Get Task by ID
- **Endpoint**: `GET /tasks/{id}`
- **Description**: Retrieves a task by its ID.

### Update Task
- **Endpoint**: `PUT /tasks/{id}`
- **Description**: Updates an existing task.

### Delete Task
- **Endpoint**: `DELETE /tasks/{id}`
- **Description**: Deletes a task by its ID.

## Usage Examples

### Register a new user
```bash
curl -X POST "http://localhost:8000/auth/register" -H "Content-Type: application/json" -d '{"username": "john", "email": "john@example.com", "password": "password123"}'
