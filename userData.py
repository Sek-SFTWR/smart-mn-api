
mock_user_data = {}

def add_user(email: str, name: str, password: str):
    mock_user_data[email] = {
        "name": name,
        "password": password
    }

def get_user(email: str):
    return mock_user_data.get(email)
