import os
import sys
import uvicorn

# Ensure the backend app is in the path
backend_path = os.path.join(os.path.dirname(__file__), "gigsecure-backend")
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print("Starting GigSecure Unified Service...")
    print(f"Access the app at: http://localhost:{port}")
    # Disable reload for maximum stability in production environments
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)
