import requests

# Replace with your Django API base URL
BASE_URL = 'http://localhost:8000/api/'

# Function to register a user
def register_user(email, username, password, first_name, last_name, phone_number, address, state, city, pincode):
    url = BASE_URL + 'register/'
    data = {
        'email': email,
        'username': username,
        'password': password,
        'first_name': first_name,
        'last_name': last_name,
        'phone_number': phone_number,
        'address': address,
        'state': state,
        'city': city,
        'pincode': pincode
    }
    response = requests.post(url, data=data)
    return response.json()

# Function to login a user
def login_user(email, password):
    url = BASE_URL + 'login/'
    data = {
        'email': email,
        'password': password
    }
    response = requests.post(url, data=data)
    return response.json()

# Test user registration and login
if __name__ == '__main__':
    # Example registration data
    registration_data = {
        'email': 'testuser@example.com',
        'username': 'testuser',
        'password': 'testpassword',
        'first_name': 'Test',
        'last_name': 'User',
        'phone_number': '1234567890',
        'address': '123 Main St',
        'state': 'State',
        'city': 'City',
        'pincode': '12345'
    }

    # Register a user
    registration_response = register_user(**registration_data)
    print('User Registration Response:', registration_response)

    # Example login data
    login_data = {
        'email': 'testuser@example.com',
        'password': 'testpassword'
    }

    # Login the registered user
    login_response = login_user(**login_data)
    print('User Login Response:', login_response)
