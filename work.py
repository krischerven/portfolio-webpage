#!/usr/bin/env python3

from config import REMOTE_TSCOMPILE
import logging
import os

logging.basicConfig()
logger = logging.getLogger("portfolio-webpage")
logger.setLevel(logging.DEBUG)


def server_work(tscompile=True):
    "Runs important server work before the webpage goes live."
    if os.path.exists(".server-work.lock"):
        logger.debug(".server-work.lock exists; skipping running server_work()")
        return
    # NOTE: 0644 is default
    open(".server-work.lock", "w")
    # This is 1) fast 2) never errors, so put it first
    logger.debug("Running ./create-download-hardlinks")
    os.system("./create-download-hardlinks")
    #
    logger.debug("Running git pull...")
    os.system("git pull")
    if tscompile:
        if os.system("which npx > /dev/null 2>&1") == 256:
            logger.debug("npx (npm) does not exist in the system path, so ./tscompile is "
                         "unrunnable. Aborting. Please install npm or make npx available "
                         "in the system path.")
            os.remove(".server-work.lock")
            exit(1)
        logger.debug("Running npm install...")
        os.system("sudo npm install")
        if os.system("which tsc > /dev/null 2>&1") == 256:
            logger.debug("tsc does not exist in the system path;"
                         "installing it globally...")
            os.system("sudo npm install -g typescript")
        logger.debug("Running ./tscompile...")
        if os.system("./tscompile") == 256:
            logger.debug("./tscompile failed to run, aborting.")
            os.remove(".server-work.lock")
            exit(1)
    else:
        logger.debug("tscompile is False (see config.py), so skipping everything else.")

    logger.debug("All done.")
    if os.path.exists(".server-work.lock"):
        os.remove(".server-work.lock")


if __name__ == "__main__":
    server_work(tscompile=REMOTE_TSCOMPILE)
