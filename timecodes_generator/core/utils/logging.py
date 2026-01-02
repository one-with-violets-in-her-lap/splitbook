import logging


def configure_logging(log_file_path: str | None = None, log_level=logging.INFO):
    """
    Configures logging to a file if `log_file_path` is specified
    Otherwise, logs don't appear anywhere
    """

    if log_file_path is not None:
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s: [%(levelname)s] %(name)s - %(message)s",
            datefmt="%m/%d/%Y %I:%M:%S %p",
            filename=log_file_path,
            filemode="w",
        )
