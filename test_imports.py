"""Test that all imports work correctly."""

try:
    from app.main import app

    print("✅ All imports successful!")
    print(f"✅ App title: {app.title}")
    print(f"✅ App version: {app.version}")
except Exception as e:
    print(f"❌ Import failed: {e}")
    import traceback

    traceback.print_exc()
