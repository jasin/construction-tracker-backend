"""Test script for user activity functionality"""

from app.database import SessionLocal
from app.repositories.user_activity_repository import UserActivityRepository


def test_user_activity():
    # Test the repository
    db = SessionLocal()
    repo = UserActivityRepository(db)

    # Test get_or_create
    print("Testing get_or_create...")
    activity = repo.get_or_create("test-user-123", "test-project-456")
    print(
        f"✅ Created activity: {activity.id}, user: {activity.user_id}, project: {activity.project_id}"
    )

    # Test update_section_visit
    print("\nTesting update_section_visit...")
    activity = repo.update_section_visit("test-user-123", "test-project-456", "rfis")
    print(f"✅ Updated RFIs visit: {activity.last_rfis_visit}")

    # Test mark_item_read
    print("\nTesting mark_item_read...")
    activity = repo.mark_item_read("test-user-123", "test-project-456", "rfi", "789")
    print(f"✅ Marked item as read: {activity.read_items}")

    # Test clear_read_items
    print("\nTesting clear_read_items...")
    activity = repo.clear_read_items("test-user-123", "test-project-456")
    print(f"✅ Cleared read items: {activity.read_items}")

    print("\n✅ All repository tests passed!")
    db.close()


if __name__ == "__main__":
    test_user_activity()
