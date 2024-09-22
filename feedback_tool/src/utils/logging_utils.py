import logging


def create_logger(namespace):
    """Function to create a logger with the given namespace."""

    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s %(message)s')

    # Create a stream handler to write to stdout
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger = logging.getLogger(namespace)
    logger.setLevel(logging.DEBUG)

    # Avoid adding multiple handlers to the logger
    if not logger.hasHandlers():
        logger.addHandler(stream_handler)

    return logger
