
from prometheus_client import CollectorRegistry, Counter

from dotenv import load_dotenv
import os

load_dotenv()

USE_PROMETHEUS = os.getenv("USE_PROMETHEUS", "False") == "True"

registry = CollectorRegistry()
commands_count = Counter(
    "commands_count",
    "Count of commands",
    [
        "command",
        "status" # ok / error
    ],
    registry=registry,
)

database_requests = Counter(
    "database_requests",
    "Count of database requests",
    [
        "status" # ok / error
    ],
    registry=registry,
)
