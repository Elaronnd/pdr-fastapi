from yaml import safe_load

file_path = "app/config/config.yml"

with open(file_path, "r", encoding="utf-8") as file:
    config_data = safe_load(file)

DB_USERNAME = config_data["db_username"]
DB_PASSWORD = config_data["db_password"]
DB_ADDRESS = config_data["db_address"]
DB_PORT = config_data["db_port"]
DB_NAME = config_data["db_name"]
JWT_PRIVATE_KEY = config_data["jwt_private_key"]
JWT_PUBLIC_KEY = config_data["jwt_public_key"]
ACCESS_TOKEN_EXPIRE_MINUTES = 30
STATUS_CODE = {
    "user not found": 404,
    "user already exists": 409,
    "this email already registered": 409,
    "invalid price": 400,
    "invalid category_id": 400,
    "unknown product_id": 404,
    "product not found": 404,
    "question not found": 404,
    "questions not found": 404,
    "you do not have permission to perform this action": 403
}