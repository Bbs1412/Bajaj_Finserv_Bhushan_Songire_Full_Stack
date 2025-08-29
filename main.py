import os
import re
import pytz
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import datetime
from slowapi import Limiter
from slowapi.util import get_remote_address


# --------------------------------------------------------------------------------
# Utility Functions
# --------------------------------------------------------------------------------

def get_ist_time():
    """Generate current time in IST

    Returns:
        str: Current IST time formatted as YYYY-MM-DD HH:MM:SS TZ
    """
    ist_timezone = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(ist_timezone)
    return current_time.strftime("%Y-%m-%d %H:%M:%S %Z")


def build_user_id(full_name: str, dob: str) -> str:
    """Build user_id string in required format
    - Converts full name to lowercase and replaces spaces with underscores
    - Appends DOB in ddmmyyyy format

    Args:
        full_name (str): Full name of user
        dob (str): Date of birth in ddmmyyyy

    Returns:
        str: user_id in format full_name_ddmmyyyy
    """
    name = "_".join(full_name.lower().split())
    return f"{name}_{dob}"


def classify_input(data):
    """Classify input data into even, odd, alphabets, and special characters.
    Also compute sum of numbers and concatenated string.

    Args:
        data (list): List of input items (strings)

    Returns:
        dict: Classification results with arrays and computed fields
    """
    NUM_RE = re.compile(r'^-?\d+$')
    ALPHA_RE = re.compile(r'^[A-Za-z]+$')

    even_numbers, odd_numbers, alphabets, special_characters = [], [], [], []
    total = 0
    letters_in_input = []

    for item in data:
        s = str(item)

        # Collect alphabetical characters from any input element for concat_string
        for ch in s:
            if ch.isalpha():
                letters_in_input.append(ch)

        if NUM_RE.match(s):
            n = int(s)
            total += n
            if n % 2 == 0:
                even_numbers.append(str(n))
            else:
                odd_numbers.append(str(n))
        elif ALPHA_RE.match(s):
            alphabets.append(s.upper())
        else:
            special_characters.append(s)

    # Build concat_string
    letters_reversed = list(reversed(letters_in_input))
    concat_chars = []
    for idx, ch in enumerate(letters_reversed):
        concat_chars.append(ch.upper() if idx % 2 == 0 else ch.lower())

    return {
        "odd_numbers": odd_numbers,
        "even_numbers": even_numbers,
        "alphabets": alphabets,
        "special_characters": special_characters,
        "sum": str(total),
        "concat_string": ''.join(concat_chars)
    }


# --------------------------------------------------------------------------------
# Config
# --------------------------------------------------------------------------------

FULL_NAME = "_".join("John Doe".split()).lower()
DOB = "17091999"
EMAIL = "john@xyz.com"
ROLL_NUMBER = "ABCD123"
RATE_LIMIT = "10000/hour"


# --------------------------------------------------------------------------------
# FastAPI + Limiter
# --------------------------------------------------------------------------------

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="BFHL FastAPI Server")
app.state.limiter = limiter


# --------------------------------------------------------------------------------
# Request Model
# --------------------------------------------------------------------------------

class DataRequest(BaseModel):
    data: list


# --------------------------------------------------------------------------------
# Endpoints
# --------------------------------------------------------------------------------

@app.get("/")
async def root():
    """Root endpoint that returns a hello message and current timestamp in IST

    Returns:
        dict: JSON response with greeting, IST timestamp, and timezone
    """
    return {
        "message": "Hello from FastAPI server!",
        "timestamp": get_ist_time(),
        "timezone": "IST (Indian Standard Time)"
    }


@app.post("/bfhl")
@limiter.limit(RATE_LIMIT)
async def bfhl(request: Request, payload: DataRequest):
    """BFHL endpoint that processes the input array.
    - Classifies data into categories
    - Builds user_id, returns email and roll number
    - Handles edge cases gracefully

    Args:
        request (Request): FastAPI request object
        payload (DataRequest): JSON body with key 'data'

    Returns:
        JSONResponse: Response with classification results and metadata
    """
    try:
        result = classify_input(payload.data)

        response = {
            "is_success": True,
            "user_id": build_user_id(FULL_NAME, DOB),
            "email": EMAIL,
            "roll_number": ROLL_NUMBER,
            **result
        }
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        return JSONResponse(
            content={
                "is_success": False,
                "error": "Internal server error",
                "details": str(e),
                "user_id": build_user_id(FULL_NAME, DOB)
            },
            status_code=500
        )


# --------------------------------------------------------------------------------
# Run Server
# --------------------------------------------------------------------------------

if __name__ == "__main__":
    print("FastAPI server is starting...")
    print("Access the API at: http://localhost:8000")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

# uvicorn main:app --host 0.0.0.0 --port 8000 --reload
