from enum import Enum


class UserRole(str, Enum):
    """User roles for authentication and authorization"""

    ADMIN = "admin"
    PROJECT_MANAGER = "project-manager"
    SUPERINTENDENT = "superintendent"
    FOREMAN = "foreman"
    USER = "user"


class ProjectPhase(str, Enum):
    """Project phases"""

    PRE_CONSTRUCTION = "pre-construction"
    CONSTRUCTION = "construction"
    CLOSE_OUT = "close-out"
    COMPLETE = "complete"


class ProjectStatus(str, Enum):
    """Project status"""

    ACTIVE = "active"
    ON_HOLD = "on-hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TaskStatus(str, Enum):
    """Task statuses"""

    TODO = "todo"
    IN_PROGRESS = "in-progress"
    REVIEW = "review"
    COMPLETE = "complete"
    ON_HOLD = "on-hold"


class TaskPriority(str, Enum):
    """Task priorities"""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class RFIStatus(str, Enum):
    """RFI (Request for Information) statuses"""

    OPEN = "open"
    PENDING = "pending"
    ANSWERED = "answered"
    CLOSED = "closed"


class RFIPriority(str, Enum):
    """RFI priorities"""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class SubmittalStatus(str, Enum):
    """Submittal statuses"""

    PENDING = "pending"
    REVIEWED = "reviewed"
    APPROVED = "approved"
    REJECTED = "rejected"


class ChangeOrderStatus(str, Enum):
    """Change order statuses"""

    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    IMPLEMENTED = "implemented"


class DocumentCategory(str, Enum):
    """Document categories"""

    DRAWING = "drawing"
    SPECIFICATION = "specification"
    CONTRACT = "contract"
    PHOTO = "photo"
    REPORT = "report"
    OTHER = "other"


class ActivityAction(str, Enum):
    """Activity log action types"""

    # Project actions
    PROJECT_CREATED = "project_created"
    PROJECT_UPDATED = "project_updated"
    PROJECT_DELETED = "project_deleted"

    # Task actions
    TASK_CREATED = "task_created"
    TASK_UPDATED = "task_updated"
    TASK_DELETED = "task_deleted"
    TASK_ASSIGNED = "task_assigned"
    TASK_COMPLETED = "task_completed"

    # RFI actions
    RFI_CREATED = "rfi_created"
    RFI_UPDATED = "rfi_updated"
    RFI_DELETED = "rfi_deleted"
    RFI_ANSWERED = "rfi_answered"

    # Submittal actions
    SUBMITTAL_CREATED = "submittal_created"
    SUBMITTAL_UPDATED = "submittal_updated"
    SUBMITTAL_DELETED = "submittal_deleted"
    SUBMITTAL_REVIEWED = "submittal_reviewed"

    # Change order actions
    CHANGE_ORDER_CREATED = "change_order_created"
    CHANGE_ORDER_UPDATED = "change_order_updated"
    CHANGE_ORDER_DELETED = "change_order_deleted"
    CHANGE_ORDER_APPROVED = "change_order_approved"

    # Document actions
    DOCUMENT_UPLOADED = "document_uploaded"
    DOCUMENT_DELETED = "document_deleted"

    # User actions
    USER_LOGIN = "user_login"
    USER_LOGOUT = "user_logout"
