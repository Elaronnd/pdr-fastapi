from yaml import safe_load

file_path = "pdr-fastapi/app/config/config.yml"

with open(file_path, "r", encoding="utf-8") as file:
    config_data = safe_load(file)

DB_USERNAME = config_data["db_username"]
DB_PASSWORD = config_data["db_password"]
DB_ADDRESS = config_data["db_address"]
DB_PORT = config_data["db_port"]
DB_NAME = config_data["db_name"]