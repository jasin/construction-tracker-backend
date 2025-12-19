# Phase 3: Pydantic Schemas - COMPLETE ✅

## Summary

All Pydantic schema classes have been successfully created, providing comprehensive request/response validation for the Construction Tracker API.

## Created Schemas

### 1. Base Schemas
**File**: `app/schemas/base.py` (2,942 bytes)

Foundation schemas used by all entities:
- **BaseSchema** - Base configuration with ORM mode enabled
- **TimestampSchema** - Adds created_at, updated_at fields
- **MetadataSchema** - Adds full metadata (created_by, updated_by)
- **BaseCreateSchema** - For POST requests (no ID/metadata)
- **BaseUpdateSchema** - For PATCH/PUT requests (all optional)
- **BaseResponseSchema** - For responses (includes ID + metadata)
- **PaginatedResponse** - Generic paginated response wrapper
- **MessageResponse** - Simple success message response
- **ErrorResponse** - Error response with details

**Configuration**:
- `from_attributes=True` - Enables ORM mode for SQLAlchemy models
- `populate_by_name=True` - Allows field population by alias
- `str_strip_whitespace=True` - Auto-strips whitespace from strings

### 2. Task Schemas
**File**: `app/schemas/task.py` (5,326 bytes)

- **TaskCreateSchema** - Create new task
  - Required: title, project_id
  - Defaults: priority=MEDIUM, status=TODO, dependencies=[]
  - Validation: title not empty, dependencies must be list
  
- **TaskUpdateSchema** - Update existing task
  - All fields optional
  - Validation: title not empty if provided
  
- **TaskResponseSchema** - Full task details
- **TaskListResponseSchema** - Simplified for lists (excludes description, estimated_hours, dependencies)

### 3. Project Schemas
**File**: `app/schemas/project.py` (4,766 bytes)

- **ProjectCreateSchema** - Create new project
  - Required: name, job_number
  - Defaults: phase=PRE_CONSTRUCTION, status='active'
  - Validation: name and job_number not empty
  
- **ProjectUpdateSchema** - Update existing project
  - All fields optional
  - Validation: name and job_number not empty if provided
  
- **ProjectResponseSchema** - Full project details
- **ProjectListResponseSchema** - Simplified for lists (excludes client_id, cost, superintendent, architect)

### 4. User Schemas
**File**: `app/schemas/user.py` (4,693 bytes)

- **UserCreateSchema** - Create new user
  - Required: email, name, password
  - Defaults: role=USER, active=True
  - Validation: email format, password min 8 chars, name not empty
  
- **UserUpdateSchema** - Update existing user
  - All fields optional
  - Validation: same as create if provided
  
- **UserResponseSchema** - Full user details (excludes password_hash)
- **UserListResponseSchema** - Simplified for lists (excludes photo)
- **UserLoginSchema** - Login credentials (email, password)
- **UserLoginResponseSchema** - Login response with JWT token
- **PasswordChangeSchema** - Change password (current_password, new_password)

**Security**: Password fields are never included in response schemas

### 5. RFI Schemas
**File**: `app/schemas/rfi.py` (4,392 bytes)

- **RFICreateSchema** - Create new RFI
  - Required: title, project_id, submitted_by
  - Defaults: priority=MEDIUM, status=OPEN
  - Validation: title not empty
  
- **RFIUpdateSchema** - Update existing RFI
  - All fields optional
  
- **RFIResponseSchema** - Full RFI details
- **RFIListResponseSchema** - Simplified for lists (excludes description, response)

### 6. Submittal Schemas
**File**: `app/schemas/submittal.py` (4,125 bytes)

- **SubmittalCreateSchema** - Create new submittal
  - Required: title, project_id
  - Defaults: status=DRAFT
  - Validation: title not empty
  
- **SubmittalUpdateSchema** - Update existing submittal
  - All fields optional
  
- **SubmittalResponseSchema** - Full submittal details
- **SubmittalListResponseSchema** - Simplified for lists (excludes description, reviewed_by, reviewed_date)

### 7. Change Order Schemas
**File**: `app/schemas/change_order.py` (4,496 bytes)

- **ChangeOrderCreateSchema** - Create new change order
  - Required: title, project_id
  - Defaults: status=PENDING
  - Validation: title not empty
  
- **ChangeOrderUpdateSchema** - Update existing change order
  - All fields optional
  
- **ChangeOrderResponseSchema** - Full change order details
- **ChangeOrderListResponseSchema** - Simplified for lists (excludes description, approved_by, approved_date)

### 8. Document Schemas
**File**: `app/schemas/document.py` (4,434 bytes)

- **DocumentCreateSchema** - Create new document
  - Required: name, type, category, url, project_id
  - Validation: name not empty, size >= 0
  
- **DocumentUpdateSchema** - Update existing document
  - All fields optional
  
- **DocumentResponseSchema** - Full document details
- **DocumentListResponseSchema** - Simplified for lists (excludes url, linked_entity_id)

### 9. Activity Log Schemas
**File**: `app/schemas/activity_log.py` (4,604 bytes)

- **ActivityLogCreateSchema** - Create new activity log
  - Required: project_id, user_id, user_name, action, entity_type, entity_id, description
  - Optional: timestamp (auto-generated), additional_data
  - Validation: description and user_name not empty
  
- **ActivityLogUpdateSchema** - Update activity log (rare - logs are immutable)
  - All fields optional
  
- **ActivityLogResponseSchema** - Full activity log details
- **ActivityLogListResponseSchema** - Simplified for lists (excludes additional_data)
- **ActivitySummarySchema** - Summary by user (user_id, name, count)
- **ActionSummarySchema** - Summary by action (action, count)

### 10. Package Init
**File**: `app/schemas/__init__.py` (3,208 bytes)

Central import location for all schemas - makes importing easier:
```python
from app.schemas import TaskCreateSchema, TaskResponseSchema
```

## Schema Patterns

### Three-Schema Pattern
Each entity typically has three schema types:

1. **Create Schema** (`*CreateSchema`)
   - For POST requests
   - Only required fields marked with `...`
   - Validation on input
   - No ID or metadata fields
   
2. **Update Schema** (`*UpdateSchema`)
   - For PATCH/PUT requests
   - All fields optional
   - Same validation as Create
   - No ID or metadata fields
   
3. **Response Schema** (`*ResponseSchema`)
   - For API responses
   - Includes ID and metadata (created_at, updated_at, created_by, updated_by)
   - All fields present
   - Converts SQLAlchemy models to JSON

### List vs Detail Schemas
Many entities have both:
- **ResponseSchema** - Full details (all fields)
- **ListResponseSchema** - Simplified (fewer fields for performance)

Use `ListResponseSchema` when returning arrays of items to reduce payload size.

### Field Validation
Common validators:
```python
@field_validator('field_name')
@classmethod
def field_not_empty(cls, v: str) -> str:
    """Validate field is not empty or whitespace."""
    if not v or not v.strip():
        raise ValueError('Field cannot be empty')
    return v.strip()
```

### Pydantic Configuration
All schemas inherit from `BaseSchema` with:
```python
model_config = ConfigDict(
    from_attributes=True,      # ORM mode for SQLAlchemy
    populate_by_name=True,      # Allow field aliasing
    str_strip_whitespace=True,  # Auto-strip strings
)
```

## Usage Examples

### Creating Entities
```python
from app.schemas import TaskCreateSchema

# In route handler
@router.post("/tasks", response_model=TaskResponseSchema)
async def create_task(
    task_data: TaskCreateSchema,
    db: Session = Depends(get_db)
):
    task_repo = TaskRepository(db)
    task = task_repo.create(task_data.model_dump(), user_id="current-user")
    return task
```

### Updating Entities
```python
from app.schemas import TaskUpdateSchema

@router.patch("/tasks/{task_id}", response_model=TaskResponseSchema)
async def update_task(
    task_id: str,
    task_data: TaskUpdateSchema,
    db: Session = Depends(get_db)
):
    task_repo = TaskRepository(db)
    # Only provided fields will be updated
    task = task_repo.update(task_id, task_data.model_dump(exclude_unset=True), user_id="current-user")
    return task
```

### List Responses
```python
from app.schemas import TaskListResponseSchema

@router.get("/tasks", response_model=list[TaskListResponseSchema])
async def list_tasks(
    project_id: str,
    db: Session = Depends(get_db)
):
    task_repo = TaskRepository(db)
    tasks = task_repo.get_by_project_id(project_id)
    return tasks
```

### Paginated Responses
```python
from app.schemas import PaginatedResponse, TaskListResponseSchema

@router.get("/tasks", response_model=PaginatedResponse)
async def list_tasks_paginated(
    project_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    task_repo = TaskRepository(db)
    tasks = task_repo.get_by_project_id(project_id, skip=skip, limit=limit)
    total = task_repo.count()
    
    return PaginatedResponse(
        items=[TaskListResponseSchema.model_validate(t) for t in tasks],
        total=total,
        skip=skip,
        limit=limit
    )
```

### Error Responses
```python
from app.schemas import ErrorResponse
from fastapi import HTTPException

@router.get("/tasks/{task_id}")
async def get_task(task_id: str, db: Session = Depends(get_db)):
    task_repo = TaskRepository(db)
    task = task_repo.get_by_id(task_id)
    
    if not task:
        raise HTTPException(
            status_code=404,
            detail=ErrorResponse(
                error="Task not found",
                detail=f"No task found with ID: {task_id}"
            ).model_dump()
        )
    
    return task
```

## Validation Examples

### Email Validation
```python
# Uses Pydantic's EmailStr
email: EmailStr = Field(..., description="User email address")
# Automatically validates email format
```

### String Length
```python
title: str = Field(..., min_length=1, max_length=200, description="Task title")
# Validates 1-200 characters
```

### Numeric Ranges
```python
cost: Optional[float] = Field(None, ge=0, description="Project cost")
# Validates >= 0 (non-negative)
```

### Enum Validation
```python
from app.constants.enums import TaskStatus

status: TaskStatus = Field(TaskStatus.TODO, description="Task status")
# Only allows valid enum values
```

### Custom Validators
```python
@field_validator('password')
@classmethod
def password_strength(cls, v: str) -> str:
    if len(v) < 8:
        raise ValueError('Password must be at least 8 characters')
    return v
```

## Schema Statistics

**Total Files**: 10
- Base: 1
- Entities: 8
- Package init: 1

**Total Schemas**: 45+
- Create schemas: 9
- Update schemas: 9
- Response schemas: 9
- List response schemas: 8
- Specialized schemas: 10+ (login, password change, summaries, etc.)

**Total Lines**: ~4,600
**Total Size**: ~47KB

## Next Steps

Now that schemas are complete, the next phase is to create **API Routes**:

1. **Create Route Structure**
   - `app/routes/` directory
   - Separate file for each entity
   - Main router aggregator

2. **Implement CRUD Endpoints**
   - GET /api/tasks (list)
   - GET /api/tasks/{id} (detail)
   - POST /api/tasks (create)
   - PATCH /api/tasks/{id} (update)
   - DELETE /api/tasks/{id} (delete)

3. **Add Specialized Endpoints**
   - Search, filter, aggregate endpoints
   - Relationship endpoints (e.g., /api/projects/{id}/tasks)

4. **Authentication & Authorization**
   - JWT token generation
   - Protected route decorators
   - Role-based access control

5. **Error Handling**
   - Consistent error responses
   - HTTP status codes
   - Validation error formatting

---

**Schema Layer: COMPLETE ✅**
**Ready for**: API Route implementation
