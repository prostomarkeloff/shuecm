import logging

from vk import VK
from vk.bot_framework import Dispatcher
from vk.utils import TaskManager

from db.prestart import pre_start as pre_start_db
from shuecm.config import LOGGING_LEVEL
from shuecm.config import PRODUCTION
from shuecm.config import SENTRY_DSN
from shuecm.config import VK_GROUP_ID
from shuecm.config import VK_TOKEN

logging.basicConfig(level=LOGGING_LEVEL)
logger = logging.getLogger("shuecm.app")

vk = VK(VK_TOKEN)
dp = Dispatcher(vk, VK_GROUP_ID)


def setup_sentry():
    if PRODUCTION and SENTRY_DSN:
        import sentry_sdk

        sentry_sdk.init(SENTRY_DSN)
        logger.info("Sentry succesfully initialized!")
    else:
        logger.info(
            "Sentry DSN not found or PRODUCTION variable is false. Sentry do not initialized."
        )


def setup_blueprints():
    from shuecm.blueprints import info_bp

    dp.setup_blueprint(info_bp)
    logger.info("Informational blueprint succesfully initialized!")


def setup_middlewares():
    from shuecm.middlewares import (
        UsersRegistrationMiddleware,
        BotAdminMiddleware,
        ChatsRegistrationMiddleware,
    )

    dp.setup_middleware(BotAdminMiddleware())
    dp.setup_middleware(ChatsRegistrationMiddleware())
    dp.setup_middleware(UsersRegistrationMiddleware())


def setup_rules():
    from shuecm.rules import Texts, UserHavePermission

    dp.setup_rule(UserHavePermission)
    dp.setup_rule(Texts)


async def run():
    pre_start_db(vk.loop)

    setup_sentry()
    setup_rules()
    setup_blueprints()
    setup_middlewares()

    dp.run_polling()


if __name__ == "__main__":
    manager = TaskManager(vk.loop)
    manager.add_task(run)
    manager.run()
