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
    """
    Setup sentry in application.

    # TODO: move to utils.py.
    :return:
    """
    if PRODUCTION and SENTRY_DSN:
        import sentry_sdk

        sentry_sdk.init(SENTRY_DSN)
        logger.info("Sentry succesfully initialized!")
    else:
        logger.info(
            "Sentry DSN not found or PRODUCTION variable is false. Sentry do not initialized."
        )


def setup_blueprints():
    """
    Register blueprints in applcation.
    :return:
    """
    from shuecm.blueprints import info_bp, user_bp, admin_bp, role_bp

    dp.setup_blueprint(info_bp)
    logger.info("Informational blueprint succesfully initialized!")

    dp.setup_blueprint(user_bp)
    logger.info("User blueprint succesfully initialized!")

    dp.setup_blueprint(admin_bp)
    logger.info("Administration blueprint succesfully initialized!")

    dp.setup_blueprint(role_bp)
    logger.info("Role blueprint succesfully initialized!")


def setup_middlewares():
    """
    Register middlewares in application.
    :return:
    """
    from shuecm.middlewares import (
        UsersRegistrationMiddleware,
        BotAdminMiddleware,
        ChatsRegistrationMiddleware,
    )

    dp.setup_middleware(BotAdminMiddleware())
    dp.setup_middleware(ChatsRegistrationMiddleware())
    dp.setup_middleware(UsersRegistrationMiddleware())


def setup_rules():
    """
    Register rules for blueprints
    :return:
    """
    from shuecm.rules import Texts, UserHavePermission, TextsWithArgs

    dp.setup_rule(UserHavePermission)
    dp.setup_rule(TextsWithArgs)
    dp.setup_rule(Texts)


async def run():
    # check database before start
    await pre_start_db(vk.loop)

    # setup sentry error tracking
    setup_sentry()
    # setup bot rules; blueprints doesn`t work without rules.
    setup_rules()
    # setup blueprints (add commands to bot)
    setup_blueprints()
    # setup middlewares for user authorization, etc.
    setup_middlewares()

    if not PRODUCTION:
        # Polling used only for tests.
        # Do not use it in production, polling may skip any events (thanks to VK-API ;) )
        # Also polling not scalable, really.
        dp.run_polling()
    elif PRODUCTION:
        # We use rabbitmq for event dispatching.
        # You can run this code in many processes (via multiprocessing module)
        # for more performance or run many instances of application.
        from vk.bot_framework.extensions.rabbitmq import RabbitMQ

        dp.setup_extension(RabbitMQ)
        dp.run_extension("rabbitmq", vk=vk, queue_name="test_queue")


def start():
    """Run many workers of rabbitmq receiver"""
    manager = TaskManager(vk.loop)
    manager.add_task(run)
    manager.run()


if __name__ == "__main__":
    # Wrapper over asyncio
    if PRODUCTION:
        import multiprocessing as mp

        processes = []
        for i in range(1, 6):
            process = mp.Process(target=start)
            processes.append(process)
            logger.info(f"[{i}] process added!")
        for index, process in enumerate(processes, start=1):
            process.start()
            logger.info(f"[{index}] process started!")
    else:
        manager = TaskManager(vk.loop)
        manager.add_task(run)
        manager.run()
