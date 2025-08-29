import pytz
import uvicorn
from fastapi import FastAPI
from datetime import datetime


def get_ist_time():
    """Generate current time in IST"""
    ist_timezone = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(ist_timezone)
    return current_time.strftime("%Y-%m-%d %H:%M:%S %Z")


# Create FastAPI instance
app = FastAPI(title="Minimal FastAPI Server")


# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint that returns a hello message and current timestamp in IST
    """
    return {
        "message": "Hello from FastAPI server!",
        "timestamp": get_ist_time(),
        "timezone": "IST (Indian Standard Time)"
    }

# To run the server directly when the script is executed
if __name__ == "__main__":
    print("FastAPI server is starting...")
    print("Access the API at: http://localhost:8000")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

# uvicorn main:app --host 0.0.0.0 --port 8000 --reload
