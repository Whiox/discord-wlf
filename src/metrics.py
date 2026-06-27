
from prometheus_client import CollectorRegistry, Counter


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
