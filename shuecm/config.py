from environs import Env

env_bot: Env = Env()
env_bot.read_env(".bot.env", recurse=False)

VK_TOKEN: str = env_bot("VK_TOKEN")
VK_GROUP_ID: int = env_bot.int("VK_GROUP_ID")
LOGGING_LEVEL: str = env_bot("LOGGING_LEVEL")

env_general: Env = Env()
env_general.read_env(".general.env", recurse=False)

SENTRY_DSN: str = env_general("SENTRY_DSN")
PRODUCTION: bool = env_general.bool("PRODUCTION")
