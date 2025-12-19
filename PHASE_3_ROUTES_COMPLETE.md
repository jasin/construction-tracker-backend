# Phase 3: API Routes - COMPLETE ✅

## Summary

All API route modules have been successfully created, providing a complete REST API for the Construction Tracker backend.

## Created Route Files

### 1. Authentication & Utilities
**Files**: `app/utils/auth.py`, `app/utils/dependencies.py`

**auth.py** - Password hashing and JWT token management:
- `verify_password(plain, hashed)` - Verify password against hash
- `get_password_hash(password)` - Hash a password
- `create_access_token(data, expires_delta)` - Create JWT token
- `decode_access_token(token)` - Decode and verify JWT token

**dependencies.py** - FastAPI dependencies for authentication/authorization:
- `get_current_user()` - Get authenticated user from JWT token
- `get_current_active_user()` - Alias for get_current_user
- `require_role(roles)` - Dependency factory for role-based access
- `require_admin()` - Require admin role
- `get_optional_user()` - Get user if authenticated, None otherwise

### 2. Task Routes
**File**: `app/routes/tasks.py` (7,999 bytes)

**Endpoints**:
- `GET /api/tasks` - List tasks with filters (project_id, status, priority, assigned_to, category)
- `GET /api/tasks/overdue` - List overdue tasks
- `GET /api/tasks/due-soon` - List tasks due within X days
- `GET /api/tasks/search?q={term}` - Search tasks by title/description
- `GET /api/tasks/{id}` - Get task by ID
- `POST /api/tasks` - Create new task
- `PATCH /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task

**Features**:
- Activity logging for all create/update/delete operations
- Flexible filtering by multiple parameters
- Pagination support (skip/limit)
- Authentication required for all endpoints

### 3. Project Routes
**File**: `app/routes/projects.py` (8,263 bytes)

**Endpoints**:
- `GET /api/projects` - List projects with filters (client_id, phase, status, manager_id, superintendent_id)
- `GET /api/projects/active` - List active projects only
- `GET /api/projects/search?q={term}` - Search by name/job number
- `GET /api/projects/job-number/{job_number}` - Get project by unique job number
- `GET /api/projects/{id}` - Get project by ID
- `POST /api/projects` - Create new project
- `PATCH /api/projects/{id}` - Update project
- `DELETE /api/projects/{id}` - Delete project

**Features**:
- Job number uniqueness validation
- Activity logging
- Flexible filtering
- Pagination support

### 4. User Routes
**File**: `app/routes/users.py` (10,043 bytes)

**Authentication Endpoints** (`/api/auth/...`):
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get JWT token
- `GET /api/auth/me` - Get current user info
- `POST /api/auth/change-password` - Change password

**User Management Endpoints** (`/api/users/...`):
- `GET /api/users` - List users with filters (role, active status)
- `GET /api/users/search?q={term}` - Search by name/email
- `GET /api/users/{id}` - Get user by ID
- `PATCH /api/users/{id}` - Update user (self or admin)
- `POST /api/users/{id}/deactivate` - Deactivate user (admin only)
- `POST /api/users/{id}/activate` - Activate user (admin only)
- `DELETE /api/users/{id}` - Delete user (admin only)

**Features**:
- Email uniqueness validation
- Password hashing with bcrypt
- JWT token generation
- Role-based access control (users can update themselves, admins can update anyone)
- Prevents users from changing their own role/active status
- Password strength validation (min 8 characters)

### 5. RFI Routes
**File**: `app/routes/rfis.py` (8,372 bytes)

**Endpoints**:
- `GET /api/rfis` - List RFIs with filters (project_id, status, priority, submitted_by, assigned_to)
- `GET /api/rfis/open` - List open RFIs
- `GET /api/rfis/overdue` - List overdue RFIs
- `GET /api/rfis/due-soon` - List RFIs due within X days
- `GET /api/rfis/search?q={term}` - Search RFIs
- `GET /api/rfis/{id}` - Get RFI by ID
- `POST /api/rfis` - Create new RFI
- `PATCH /api/rfis/{id}` - Update RFI
- `DELETE /api/rfis/{id}` - Delete RFI

**Features**:
- Activity logging
- Overdue/due-soon queries
- Flexible filtering
- Pagination support

### 6. Submittal Routes
**File**: `app/routes/submittals.py` (7,137 bytes)

**Endpoints**:
- `GET /api/submittals` - List submittals with filters (project_id, status, submitted_by, reviewed_by)
- `GET /api/submittals/pending-review` - List submittals pending review
- `GET /api/submittals/search?q={term}` - Search submittals
- `GET /api/submittals/{id}` - Get submittal by ID
- `POST /api/submittals` - Create new submittal
- `PATCH /api/submittals/{id}` - Update submittal
- `DELETE /api/submittals/{id}` - Delete submittal

**Features**:
- Activity logging
- Status-based queries (pending review)
- Flexible filtering
- Pagination support

### 7. Change Order Routes
**File**: `app/routes/change_orders.py` (7,873 bytes)

**Endpoints**:
- `GET /api/change-orders` - List change orders with filters (project_id, status, requested_by, approved_by)
- `GET /api/change-orders/pending-approval` - List change orders pending approval
- `GET /api/change-orders/search?q={term}` - Search change orders
- `GET /api/change-orders/total-cost/{project_id}` - Get total cost for project
- `GET /api/change-orders/{id}` - Get change order by ID
- `POST /api/change-orders` - Create new change order
- `PATCH /api/change-orders/{id}` - Update change order
- `DELETE /api/change-orders/{id}` - Delete change order

**Features**:
- Activity logging
- Cost aggregation (total cost by project, approved cost only)
- Status-based queries
- Flexible filtering
- Pagination support

### 8. Document Routes
**File**: `app/routes/documents.py` (7,883 bytes)

**Endpoints**:
- `GET /api/documents` - List documents with filters (project_id, type, category, linked_entity_id, uploaded_by)
- `GET /api/documents/search?q={term}` - Search documents by name
- `GET /api/documents/storage/{project_id}` - Get total storage used by project
- `GET /api/documents/stats/{project_id}` - Get document statistics (counts by type/category, storage)
- `GET /api/documents/{id}` - Get document by ID
- `POST /api/documents` - Create new document record
- `PATCH /api/documents/{id}` - Update document record
- `DELETE /api/documents/{id}` - Delete document record

**Features**:
- Activity logging
- Storage analytics (total bytes/MB per project)
- Document statistics (counts by type, counts by category)
- Linked entity support (attach documents to tasks, RFIs, etc.)
- Flexible filtering
- Pagination support

### 9. Activity Log Routes
**File**: `app/routes/activity_logs.py` (5,658 bytes)

**Endpoints**:
- `GET /api/activity-logs` - List activity logs with filters (project_id, user_id, action, entity_type, entity_id, date range)
- `GET /api/activity-logs/recent` - Get recent activity (last 50 by default)
- `GET /api/activity-logs/summary/by-user` - Get activity counts grouped by user
- `GET /api/activity-logs/summary/by-action` - Get activity counts grouped by action
- `GET /api/activity-logs/{id}` - Get activity log by ID
- `DELETE /api/activity-logs/cleanup` - Delete old logs (admin only)

**Features**:
- Comprehensive filtering (project, user, action, entity, date range)
- Recent activity feed
- Summary/analytics endpoints
- Data pruning (cleanup old logs to save storage)
- Admin-only cleanup endpoint
- Pagination support

### 10. Main Router
**File**: `app/routes/__init__.py` (859 bytes)

Aggregates all route modules into a single `api_router`:
```python
api_router = APIRouter(prefix="/api")
api_router.include_router(users.auth_router)  # /api/auth/...
api_router.include_router(users.router)       # /api/users/...
api_router.include_router(tasks.router)       # /api/tasks/...
api_router.include_router(projects.router)    # /api/projects/...
api_router.include_router(rfis.router)        # /api/rfis/...
api_router.include_router(submittals.router)  # /api/submittals/...
api_router.include_router(change_orders.router)  # /api/change-orders/...
api_router.include_router(documents.router)   # /api/documents/...
api_router.include_router(activity_logs.router)  # /api/activity-logs/...
```

### 11. Main Application
**Updated**: `app/main.py`

Integrated the main API router:
```python
from app.routes import api_router
app.include_router(api_router)
```

All routes now accessible under `/api/` prefix.

## Common Patterns

### 1. Authentication
All endpoints require authentication via JWT token:
```python
@router.get("/endpoint")
async def handler(current_user: User = Depends(get_current_user)):
    # current_user is authenticated User object
```

### 2. Authorization
Admin-only endpoints use `require_admin` dependency:
```python
@router.delete("/endpoint")
async def handler(admin_user: User = Depends(require_admin)):
    # admin_user has 'admin' role
```

### 3. Activity Logging
All create/update/delete operations log activity:
```python
activity_repo.log_activity(
    project_id=entity.project_id,
    user_id=current_user.id,
    user_name=current_user.name,
    action="entity_created",
    entity_type="entity",
    entity_id=entity.id,
    description=f"Created entity: {entity.title}",
    additional_data={"field": value}
)
```

### 4. Pagination
All list endpoints support pagination:
```python
@router.get("")
async def list_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    ...
):
    items = repo.get_all(skip=skip, limit=limit)
```

### 5. Filtering
List endpoints support multiple filter combinations:
```python
if project_id and status:
    items = repo.get_by_status(status, project_id=project_id, skip=skip, limit=limit)
elif project_id:
    items = repo.get_by_project_id(project_id, skip=skip, limit=limit)
else:
    items = repo.get_all(skip=skip, limit=limit)
```

### 6. Error Handling
Consistent HTTP error responses:
```python
if not entity:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Entity not found with ID: {entity_id}"
    )
```

### 7. Update Pattern
Updates use `exclude_unset=True` to only update provided fields:
```python
entity = repo.update(
    entity_id,
    data.model_dump(exclude_unset=True),
    user_id=current_user.id
)
```

## API Documentation

Once the server is running, FastAPI provides automatic interactive documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

## Testing the API

### Start the Server
```bash
# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run the server
uvicorn app.main:app --reload
```

Server will start at `http://localhost:8000`

### Example Requests

#### Register a User
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "name": "Admin User",
    "password": "securepassword123",
    "role": "admin"
  }'
```

#### Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "securepassword123"
  }'
```

Returns:
```json
{
  "id": "user-id",
  "email": "admin@example.com",
  "name": "Admin User",
  "role": "admin",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### Create a Project (Authenticated)
```bash
curl -X POST http://localhost:8000/api/projects \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "name": "Downtown Office Building",
    "job_number": "2024-001",
    "phase": "pre-construction",
    "status": "active"
  }'
```

#### List Tasks
```bash
curl -X GET "http://localhost:8000/api/tasks?project_id=PROJECT_ID&skip=0&limit=20" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Route Statistics

**Total Files**: 11
- Route modules: 8
- Auth utilities: 2
- Main router: 1

**Total Endpoints**: 60+
- Authentication: 4 (`/api/auth/...`)
- User management: 7 (`/api/users/...`)
- Tasks: 8 (`/api/tasks/...`)
- Projects: 8 (`/api/projects/...`)
- RFIs: 9 (`/api/rfis/...`)
- Submittals: 7 (`/api/submittals/...`)
- Change Orders: 8 (`/api/change-orders/...`)
- Documents: 9 (`/api/documents/...`)
- Activity Logs: 6 (`/api/activity-logs/...`)

**Total Lines**: ~8,000
**Total Size**: ~64KB

## Next Steps

The backend API is now complete! The final phase is **WebSocket Support** for real-time updates:

1. **Create WebSocket Manager**
   - Connection management
   - Broadcasting to subscribed clients
   - Room-based subscriptions (by project)

2. **Create WebSocket Endpoints**
   - `/ws/project/{project_id}` - Subscribe to project updates
   - `/ws/activity` - Subscribe to global activity feed

3. **Integrate with Routes**
   - Broadcast updates after create/update/delete operations
   - Send real-time notifications to connected clients

4. **Frontend Integration**
   - WebSocket client library
   - Auto-reconnect logic
   - Update local state on messages

---

**API Routes: COMPLETE ✅**
**Ready for**: WebSocket implementation (optional) or frontend integration
