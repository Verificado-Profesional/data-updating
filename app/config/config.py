from decouple import config
from pydantic import BaseSettings


class Settings(BaseSettings):
    host = config("HOST")
    port = int(config("PORT"))
    client = config("ATLAS_URI")
    db_name = config("DB_NAME")


#     print(host, port, client)
#     return host, int(port), client, db_name
# DEV_ENV = "dev"
# environment: str = DEV_ENV
# db_name: str
# port: str
# host: str
# atlas_uri: str
# # user_admin_url: str

# class Config:
#     BASE_DIR = os.path.dirname(os.path.abspath("../.env"))
#     env_file = os.path.join(BASE_DIR, ".env")
#     uri = os.getenv("ATLAS_URI")


def get_settings():
    return Settings()
