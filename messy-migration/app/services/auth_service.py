import bcrypt
from app.models.user_model import get_user_by_id

def verify_user(data):
    user_id = data.get("id")
    password = data.get("password")
    user = get_user_by_id(user_id)
    if not user:
        return False, "User not found"
    if not bcrypt.checkpw(password.encode(), user["password"].encode()):
        return False, "Invalid password"
    return True, user
