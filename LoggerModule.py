import logging

logger = logging.getLogger("healthcare_app")
logger.setLevel(logging.INFO)
logger.propagate = False

# The 'if' below stops duplicate log lines in case this module
# accidentally gets imported more than once.
if not logger.handlers:
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    log_format = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%H:%M:%S",
    )
    console_handler.setFormatter(log_format)

    logger.addHandler(console_handler)
