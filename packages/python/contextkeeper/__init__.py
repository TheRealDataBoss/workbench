"""contextkeeper — Zero model drift between AI agents."""

from contextkeeper.client import ContextKeeperClient
from contextkeeper.exceptions import (
    AuthenticationError,
    AuthorizationError,
    BackendError,
    ContextKeeperError,
    HandoffNotFoundError,
    ProjectNotInitializedError,
    RateLimitError,
    SchemaVersionError,
    SessionNotFoundError,
)
from contextkeeper.models import (
    AgentType,
    ApiKey,
    AuditEvent,
    Decision,
    Handoff,
    HandoffDiff,
    Organization,
    ProjectConfig,
    Session,
    Task,
    TaskStatus,
    User,
)

__version__ = "0.6.0"

__all__ = [
    # Client
    "ContextKeeperClient",
    # Models
    "AgentType",
    "ApiKey",
    "AuditEvent",
    "Decision",
    "Handoff",
    "HandoffDiff",
    "Organization",
    "ProjectConfig",
    "Session",
    "Task",
    "TaskStatus",
    "User",
    # Exceptions
    "AuthenticationError",
    "AuthorizationError",
    "BackendError",
    "ContextKeeperError",
    "HandoffNotFoundError",
    "ProjectNotInitializedError",
    "RateLimitError",
    "SchemaVersionError",
    "SessionNotFoundError",
]
