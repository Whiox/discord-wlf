
from prometheus_client import CollectorRegistry, Gauge

from dotenv import load_dotenv
import os

load_dotenv()

USE_PROMETHEUS = os.getenv("USE_PROMETHEUS", "False") == "True"
PUSHGW = os.getenv("PUSHGW")

registry = CollectorRegistry()
commands_count = Gauge(
    "commands_count",
    "Count of commands",
    [
        "command",
        "status" # ok / error
    ],
    registry=registry,
)

database_requests = Gauge(
    "database_requests",
    "Count of database requests",
    [
        "status" # ok / error
    ],
    registry=registry,
)
