import json

def authenticate(user_id, password):
    with open('user_data.json', 'r', encoding='utf-8') as file:
        users = json.load(file)
    
    for user in users:
        if user["user_id"] == user_id and user["password"] == password:
            return user

    return None