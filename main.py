import os
import sys
import uvicorn

# Ensure the backend app is in the path
backend_path = os.path.join(os.path.dirname(__file__), "gigpulse")
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    line = "=" * 66
    print(line)
    print("ZenVyte GigPulse - AI-Powered Parametric Income Protection v2.1.0")
    print(line)
    print(f"Open: http://localhost:{port}")
    print("API docs: http://localhost:{}/docs".format(port))
    print("")
    print("Demo credentials:")
    print("Worker: ravi.kumar@swiggy.in / demo1234")
    print("Worker: arjun.raj@zomato.in / demo1234")
    print("Admin : admin@digit.com / admin123")
    print("Press Ctrl+C to stop the server")
    print("")
    uvicorn.run(
        "gigpulse.app.main:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        access_log=False,
        log_level=os.environ.get("UVICORN_LOG_LEVEL", "error").lower(),
    )
