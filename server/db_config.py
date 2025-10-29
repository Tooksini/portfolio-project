import configparser
import os

config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(__file__), "db_config.properties")

# Load from .properties only if it exists (for local dev)
if os.path.exists(config_path):
    config.read(config_path)
else:
    config["DEFAULT"] = {}

# ✅ Automatically switch between local (.properties) and Render (.env)
DB_CONFIG = {
    "host": os.getenv("DB_HOST", config.get("DEFAULT", "host", fallback="localhost")),
    "user": os.getenv("DB_USER", config.get("DEFAULT", "user", fallback="root")),
    "password": os.getenv("DB_PASSWORD", config.get("DEFAULT", "password", fallback="")),
    "database": os.getenv("DB_NAME", config.get("DEFAULT", "database", fallback="portfolio_db")),
    "port": int(os.getenv("DB_PORT", config.get("DEFAULT", "port", fallback=3306))),
}
