import re

def validate_input(input_data):
    """Check if input data is not empty after stripping whitespace."""
    return bool(input_data and input_data.strip())

def parse_data(data):
    """Split and clean input data into a list, removing empty items."""
    return [item.strip() for item in data.split(',') if item.strip()] if data else []

def validate_login_credentials(username, password):
    """
    Validate username and password:
    - Username: At least 4 characters
    - Password: At least 6 characters, with at least one letter and one number
    """
    if not username or not password:
        return False  # Prevent NoneType errors
    
    username = username.strip()
    if len(username) < 4:
        return False  # Username must be at least 4 characters

    if len(password) < 6 or not re.search(r"[A-Za-z]", password) or not re.search(r"\d", password):
        return False  # Password must be at least 6 characters with a mix of letters & numbers

    return True
