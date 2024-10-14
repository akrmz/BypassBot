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

# Load the environment variables from config.env without overriding existing ones
load_dotenv("config.env", override=False)

UPSTREAM_REPO = getenv("UPSTREAM_REPO", "https://github.com/akrmz/BypassBot/")
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "main")

if UPSTREAM_REPO:
    # Check if the repository already exists (i.e., .git directory exists)
    if not opath.exists(".git"):
        log_info(".git directory not found, initializing repository.")
        srun(["git", "init", "-q"], shell=True)

    # Add upstream repo as remote (if it doesn't already exist)
    srun(["git", "remote", "add", "origin", UPSTREAM_REPO], shell=True)
    
    # Fetch the latest changes from upstream
    fetch_result = srun(["git", "fetch", "origin", "-q"], shell=True)
    
    # Hard reset to the latest commit on the UPSTREAM_BRANCH
    if fetch_result.returncode == 0:
        reset_result = srun(["git", "reset", "--hard", f"origin/{UPSTREAM_BRANCH}", "-q"], shell=True)
        if reset_result.returncode == 0:
            log_info("Successfully updated with latest commit from UPSTREAM_REPO")
        else:
            log_error("Failed to reset to the latest commit.")
    else:
        log_error("Failed to fetch from UPSTREAM_REPO. Check if the repository is valid.")

else:
    log_error("UPSTREAM_REPO environment variable is not set.")
