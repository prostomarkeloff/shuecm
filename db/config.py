from environs import Env

env_db: Env = Env()
env_db.read_env("..database.env.example", recurse=False)

MONGODB_CONNECTION_URI: str = env_db("MONGODB_CONNECTION_URI")
MONGODB_DATABASE_NAME: str = env_db("MONGODB_DATABASE_NAME")
