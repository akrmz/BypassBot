from os import path as opath, getenv
from logging import (
    StreamHandler,
    INFO,
    basicConfig,
    error as log_error,
    info as log_info,
)
from logging.handlers import RotatingFileHandler
from subprocess import run as srun
from dotenv import load_dotenv

basicConfig(
    level=INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s [%(filename)s:%(lineno)d]",
    datefmt="%d-%b-%y %I:%M:%S %p",
    handlers=[
        RotatingFileHandler("log.txt", maxBytes=50000000, backupCount=10),
        StreamHandler(),
    ],
)
load_dotenv("config.env", override=True)

UPSTREAM_REPO = getenv("UPSTREAM_REPO", "https://github.com/akrmz/BypassBot")
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "main")

if UPSTREAM_REPO is not None:
    if opath.exists(".git"):
        srun(["rm", "-rf", ".git"])

    update = srun(
        [
        "git fetch origin -q \
        && git merge origin/{UPSTREAM_BRANCH} -q"
    ],
        shell=True,
    )

    if update.returncode == 0:
        log_info("Successfully updated with latest commit from UPSTREAM_REPO")
    else:
        log_error(
            "Something went wrong while updating, check UPSTREAM_REPO if valid or not!"
        )
