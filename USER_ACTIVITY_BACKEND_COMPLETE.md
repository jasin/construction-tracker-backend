# User Activity Backend Implementation - Complete ✅

## Overview

Successfully implemented a complete backend system for tracking user activity (read/unread items) across devices in the Construction Tracker application.

## Implementation Summary

### 1. Database Schema ✅

**Table:** `user_activity`

```sql
CREATE TABLE user_activity (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL,
  project_id UUID NOT NULL,
  
  -- Section visit timestamps
  last_rfis_visit TIMESTAMPTZ,
  last_submittals_visit TIMESTAMPTZ,
  last_change_orders_visit TIMESTAMPTZ,
  last_tasks_visit TIMESTAMPTZ,
  last_documents_visit TIMESTAMPTZ,
  
  -- Individual item reads (JSONB)
  read_items JSONB DEFAULT '{}',
  
  created_at TIMESTAMPTZ,
  updated_at TIMESTAMPTZ,
  created_by VARCHAR,
  updated_by VARCHAR,
  
  UNIQUE(user_id, project_id)
);
```

**Indexes:**
- `ix_user_activity_user_id` on `user_id`
- `ix_user_activity_project_id` on `project_id`
- `ix_user_activity_user_project` on `(user_id, project_id)`

**Migration:** `20251219_114443_add_user_activity_table.py`

### 2. SQLAlchemy Model ✅

**File:** `app/models/user_activity.py`

- Inherits from `BaseModel`
- Maps to `user_activity` table
- Includes JSONB support for flexible read_items storage
- Auto-generates UUIDs for IDs

### 3. Pydantic Schemas ✅

**File:** `app/schemas/user_activity.py`

**Schemas:**
- `SectionVisitUpdate` - Request schema for updating section visits
  - Validates section names (rfis, submittals, change_orders, tasks, documents)
- `MarkItemRead` - Request schema for marking items as read
  - Validates entity types (rfi, submittal, change_order, task, document)
- `UserActivityResponse` - Response schema with all activity data

### 4. Repository ✅

**File:** `app/repositories/user_activity_repository.py`

**Methods:**
- `get_or_create(user_id, project_id)` - Get or create activity record
- `update_section_visit(user_id, project_id, section, timestamp)` - Update section visit time
- `mark_item_read(user_id, project_id, entity_type, entity_id, timestamp)` - Mark item as read
- `get_by_user_and_project(user_id, project_id)` - Get specific activity record
- `clear_read_items(user_id, project_id)` - Clear all read items
- `clear_section_visits(user_id, project_id)` - Clear all section visits

### 5. API Endpoints ✅

**File:** `app/routes/user_activity.py`

**Base URL:** `/api/user-activity`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/{project_id}` | Get user activity for a project |
| PUT | `/{project_id}/section-visit` | Update section visit timestamp |
| PUT | `/{project_id}/mark-read` | Mark an item as read |
| DELETE | `/{project_id}/clear-read-items` | Clear all read items |
| DELETE | `/{project_id}/clear-section-visits` | Clear all section visits |

**Authentication:** All endpoints require JWT authentication (via `get_current_user`)

### 6. Testing ✅

**Test File:** `test_user_activity.py`

All repository methods tested successfully:
- ✅ Get or create activity record
- ✅ Update section visit timestamps
- ✅ Mark items as read (JSONB updates)
- ✅ Clear read items

## How It Works

### Tracking Section Visits

When a user navigates to a section (e.g., RFIs tab):

```javascript
// Frontend calls:
PUT /api/user-activity/{projectId}/section-visit
Body: { "section": "rfis" }

// Backend updates:
last_rfis_visit = NOW()
```

### Tracking Item Reads

When a user clicks/expands an item (e.g., opens an RFI):

```javascript
// Frontend calls:
PUT /api/user-activity/{projectId}/mark-read
Body: { "entity_type": "rfi", "entity_id": "123" }

// Backend updates JSONB:
read_items = { "rfi_123": "2025-12-19T16:50:10.859231Z" }
```

### Determining Unread Status

Frontend logic:
1. Check if item is in `read_items` → if yes, it's read
2. Check if item's `created_at` > `last_section_visit` → if yes, it's unread
3. Otherwise, it's read

## Benefits

✅ **Cross-device sync** - User sees consistent unread state on all devices  
✅ **Persistent** - Survives browser cache clears  
✅ **Scalable** - JSONB for efficient storage and queries  
✅ **Secure** - JWT authentication, users can only access their own data  
✅ **Fast** - Indexed lookups, one record per user per project  

## Database Migration

Migration successfully applied:
```bash
cd construction-tracker-backend
python -m alembic upgrade head
```

## Next Steps

**Frontend Implementation:**
1. Create `userActivityApi.js` in frontend
2. Update `useUserActivity.js` composable to use backend API
3. Test cross-device sync
4. Remove localStorage implementation

## Files Created

### Backend Files
- `migrations/versions/20251219_114443_add_user_activity_table.py`
- `app/models/user_activity.py`
- `app/schemas/user_activity.py`
- `app/repositories/user_activity_repository.py`
- `app/routes/user_activity.py`
- `test_user_activity.py`

### Updated Files
- `app/models/__init__.py` - Added UserActivity export
- `app/routes/__init__.py` - Registered user_activity routes

## API Usage Examples

### Get User Activity
```bash
GET /api/user-activity/project-123
Authorization: Bearer <jwt-token>

Response:
{
  "id": "abc-123",
  "user_id": "user-456",
  "project_id": "project-123",
  "last_rfis_visit": "2025-12-19T16:30:00Z",
  "last_submittals_visit": null,
  "read_items": {
    "rfi_789": "2025-12-19T16:45:00Z",
    "task_101": "2025-12-19T16:40:00Z"
  },
  "created_at": "2025-12-19T10:00:00Z",
  "updated_at": "2025-12-19T16:50:00Z"
}
```

### Update Section Visit
```bash
PUT /api/user-activity/project-123/section-visit
Authorization: Bearer <jwt-token>
Content-Type: application/json

{
  "section": "rfis"
}
```

### Mark Item as Read
```bash
PUT /api/user-activity/project-123/mark-read
Authorization: Bearer <jwt-token>
Content-Type: application/json

{
  "entity_type": "rfi",
  "entity_id": "789"
}
```

---

**Status:** ✅ Backend Complete - Ready for Frontend Integration
**Date:** 2025-12-19
**Migration Revision:** e4f9c8b7a1d3
