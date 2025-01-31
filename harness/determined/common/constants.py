# The maximum size of a WebSocket message that can be sent or received
# by the Determined agent and trial-runner. The master uses a different limit,
# because it uses the uwsgi WebSocket implementation; see
# `websocket-max-size` in `uwsgi.ini`.
MAX_WEBSOCKET_MSG_SIZE = 128 * 1024 * 1024

# The maximum HTTP request size that will be accepted by the master. This
# is intended as a safeguard to quickly drop overly large HTTP requests.
MAX_HTTP_REQUEST_SIZE = 128 * 1024 * 1024

# The maximum size of a model (the sum of the model definition plus any
# additional package dependencies). Models are created via HTTP and sent
# to agents via WebSockets; we also have to account for the overhead of
# base64 encoding. Models are also stored in Postgres but the max
# Postgres field size is 1GB, so we ignore that here.
MAX_ENCODED_SIZE = (min(MAX_WEBSOCKET_MSG_SIZE, MAX_HTTP_REQUEST_SIZE) // 8) * 6
# We subtract one megabyte to account for any message envelope size we may have.
MAX_CONTEXT_SIZE = MAX_ENCODED_SIZE - (1 * 1024 * 1024)

# The username and password for the default user.
DEFAULT_DETERMINED_USER = "determined"
DEFAULT_DETERMINED_PASSWORD = ""
DEFAULT_CHECKPOINT_PATH = "checkpoints"

ACTIVE = "ACTIVE"
CANCELED = "CANCELED"
COMPLETED = "COMPLETED"
DELETED = "DELETED"
ERROR = "ERROR"

TERMINAL_STATES = {COMPLETED, CANCELED, ERROR}

SHARED_FS_CONTAINER_PATH = "/determined_shared_fs"

# By default, we ignore:
#  - all byte-compiled Python files to ignore a potential stale compilation
#  - terraform files generated by `det deploy gcp`, e.g. when user creates
#    a cluster from the (tutorial) model def directory.
#  - .git and IDE-related content
# Users may also define custom .detignore files to ignore arbitrary paths.
DEFAULT_DETIGNORE = [
    "__pycache__/",
    "*.py[co]",
    "*$py.class",
    "terraform",
    "terraform_data",
    "terraform.tfstate*",
    "terraform.tfvars*",
    ".terraform*",
    ".git/",
    ".vscode/",
    ".idea/",
    ".mypy_cache/",
]
