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

# Check if the .git directory exists
if opath.exists(".git"):
    # Check if the remote already exists
    remote_check = srun(["git", "remote", "-v"], capture_output=True, text=True)
    if "origin" not in remote_check.stdout:
        # Add remote if it doesn't exist
        add_remote = srun(["git", "remote", "add", "origin", UPSTREAM_REPO], capture_output=True, text=True)
        if add_remote.returncode != 0:
            log_error(f"Failed to add remote: {add_remote.stderr}")
            exit(1)

    # Fetch the latest changes from the upstream repo
    fetch_result = srun(["git", "fetch", "origin"], capture_output=True, text=True)
    if fetch_result.returncode == 0:
        # Merge the changes into the current branch
        merge_result = srun(["git", "merge", f"origin/{UPSTREAM_BRANCH}"], capture_output=True, text=True)
        if merge_result.returncode == 0:
            log_info("Successfully updated with latest commit from UPSTREAM_REPO")
        else:
            log_error(f"Merge failed: {merge_result.stderr}")
    else:
        log_error(f"Fetch failed: {fetch_result.stderr}")
else:
    log_error("No .git directory found. Please initialize a git repository first.")
