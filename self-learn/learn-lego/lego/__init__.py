from loguru import logger
import sys
__setup__ = False

import logging
import warnings

warnings.filterwarnings("ignore")
__version__ = "1.0.0"


if not __setup__:
    for name in [
        "uvicorn.error",
        "websockets.protocol",
        "websockets.server"
    ]:
        logging.getLogger(name).addFilter(lambda record: record.msg not in [
            "connection handler failed",
            "closing handshake failed"
        ])

    try:
        import uvloop

        uvloop.install()
    except ImportError:
        pass

    logger.remove()
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level}</level> | <level>{message}</level>",
        colorize=True
    )

    __setup__ = False
