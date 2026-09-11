import logging
import os


def get_logger(name):

    os.makedirs("logs", exist_ok=True)

    logging.basicConfig(

        filename="logs/project.log",

        format="%(asctime)s %(levelname)s %(message)s",

        level=logging.INFO

    )

    return logging.getLogger(name)