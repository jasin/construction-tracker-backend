"""
Schemas package
Provides Pydantic schemas for request/response validation.
"""

from app.schemas.activity_log import (
    ActionSummarySchema,
    ActivityLogCreateSchema,
    ActivityLogListResponseSchema,
    ActivityLogResponseSchema,
    ActivityLogUpdateSchema,
    ActivitySummarySchema,
)
from app.schemas.base import (
    BaseCreateSchema,
    BaseResponseSchema,
    BaseSchema,
    BaseUpdateSchema,
    ErrorResponse,
    MessageResponse,
    MetadataSchema,
    PaginatedResponse,
    TimestampSchema,
)
from app.schemas.change_order import (
    ChangeOrderCreateSchema,
    ChangeOrderListResponseSchema,
    ChangeOrderResponseSchema,
    ChangeOrderUpdateSchema,
)
from app.schemas.document import (
    DocumentCreateSchema,
    DocumentListResponseSchema,
    DocumentResponseSchema,
    DocumentUpdateSchema,
)
from app.schemas.project import (
    ProjectCreateSchema,
    ProjectListResponseSchema,
    ProjectResponseSchema,
    ProjectUpdateSchema,
)
from app.schemas.rfi import (
    RFICreateSchema,
    RFIListResponseSchema,
    RFIResponseSchema,
    RFIUpdateSchema,
)
from app.schemas.submittal import (
    SubmittalCreateSchema,
    SubmittalListResponseSchema,
    SubmittalResponseSchema,
    SubmittalUpdateSchema,
)
from app.schemas.task import (
    TaskCreateSchema,
    TaskListResponseSchema,
    TaskResponseSchema,
    TaskUpdateSchema,
)
from app.schemas.user import (
    PasswordChangeSchema,
    UserCreateSchema,
    UserListResponseSchema,
    UserLoginResponseSchema,
    UserLoginSchema,
    UserResponseSchema,
    UserUpdateSchema,
)

__all__ = [
    # Base schemas
    "BaseSchema",
    "TimestampSchema",
    "MetadataSchema",
    "BaseCreateSchema",
    "BaseUpdateSchema",
    "BaseResponseSchema",
    "PaginatedResponse",
    "MessageResponse",
    "ErrorResponse",
    # Task schemas
    "TaskCreateSchema",
    "TaskUpdateSchema",
    "TaskResponseSchema",
    "TaskListResponseSchema",
    # Project schemas
    "ProjectCreateSchema",
    "ProjectUpdateSchema",
    "ProjectResponseSchema",
    "ProjectListResponseSchema",
    # User schemas
    "UserCreateSchema",
    "UserUpdateSchema",
    "UserResponseSchema",
    "UserListResponseSchema",
    "UserLoginSchema",
    "UserLoginResponseSchema",
    "PasswordChangeSchema",
    # RFI schemas
    "RFICreateSchema",
    "RFIUpdateSchema",
    "RFIResponseSchema",
    "RFIListResponseSchema",
    # Submittal schemas
    "SubmittalCreateSchema",
    "SubmittalUpdateSchema",
    "SubmittalResponseSchema",
    "SubmittalListResponseSchema",
    # Change Order schemas
    "ChangeOrderCreateSchema",
    "ChangeOrderUpdateSchema",
    "ChangeOrderResponseSchema",
    "ChangeOrderListResponseSchema",
    # Document schemas
    "DocumentCreateSchema",
    "DocumentUpdateSchema",
    "DocumentResponseSchema",
    "DocumentListResponseSchema",
    # Activity Log schemas
    "ActivityLogCreateSchema",
    "ActivityLogUpdateSchema",
    "ActivityLogResponseSchema",
    "ActivityLogListResponseSchema",
    "ActivitySummarySchema",
    "ActionSummarySchema",
]
