import os

API_HOST_DEFAULT = "127.0.0.1"

def get_api_url():
    host = os.environ.get("API_HOST", API_HOST_DEFAULT)
    port = 5000 if host == API_HOST_DEFAULT else 80
    return f"http://{host}:{port}"

basedir = os.path.abspath(os.path.dirname(__file__))