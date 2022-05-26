import os

API_HOST_DEFAULT = "127.0.0.1"

def get_postgres_uri():
    host = os.environ.get("DB_HOST", "localhost")
    port = 5432 if host == "localhost" else 5432
    password = os.environ.get("DB_PASSWORD", "")
    user, db_name = "allocation", "allocation"
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


def get_api_url():
    host = os.environ.get("API_HOST", API_HOST_DEFAULT)
    port = 5000 if host == API_HOST_DEFAULT else 80
    return f"http://{host}:{port}"
