# Set up Environment

1. Crate a virtual environment:
    ```powershell
    python -m venv venv
    ```

2. Activate the virtual environment:
    Windows:
    ```powershell
    .\venv\Scripts\activate
    ```
    macOS/Linux:
    ```bash
    source venv/bin/Activate
    ```

3. Install required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the FastAPI server:
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    ```

5. Check in browser:
    ```url
    http://localhost:8000
    ```


# Testing:

1. To run tests, use the command:
    ```powershell
    pytest -v test_main.py
    ```

1. To see detailed output, use:
    ```powershell
    pytest -v -s test_main.py
    ```
