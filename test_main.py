import pytest
from main import app
from fastapi.testclient import TestClient

# Initialize test client
client = TestClient(app)

# --------------------------------------------------------------------------------
# Test Data:
# --------------------------------------------------------------------------------

# Test Case - 1
test_data = {
    "data": ["a", "1", "334", "4", "R", "$"]
}

expected_result = {
    "is_success": True,
    "user_id": "john_doe_17091999",
    "email": "john@xyz.com",
    "roll_number": "ABCD123",
    "odd_numbers": ["1"],
    "even_numbers": ["334", "4"],
    "alphabets": ["A", "R"],
    "special_characters": ["$"],
    "sum": "339",
    "concat_string": "Ra"
}


# Test Case - 2
test_data_2 = {
    "data": ["2", "a", "y", "4", "&", "-", "*", "5", "92", "b"]
}

expected_result_2 = {
    "is_success": True,
    "user_id": "john_doe_17091999",
    "email": "john@xyz.com",
    "roll_number": "ABCD123",
    "odd_numbers": ["5"],
    "even_numbers": ["2", "4", "92"],
    "alphabets": ["A", "Y", "B"],
    "special_characters": ["&", "-", "*"],
    "sum": "103",
    "concat_string": "ByA"
}

# Test Case - 3
test_data_3 = {
    "data": ["A", "ABcD", "DOE"]
}

expected_result_3 = {
    "is_success": True,
    "user_id": "john_doe_17091999",
    "email": "john@xyz.com",
    "roll_number": "ABCD123",
    "odd_numbers": [],
    "even_numbers": [],
    "alphabets": ["A", "ABCD", "DOE"],
    "special_characters": [],
    "sum": "0",
    "concat_string": "EoDdCbAa"
}


# --------------------------------------------------------------------------------
# Tests
# --------------------------------------------------------------------------------

@pytest.mark.parametrize("test_input,expected", [
    (test_data, expected_result),
    (test_data_2, expected_result_2),
    (test_data_3, expected_result_3)
])
def test_bfhl_endpoint_parametrized(test_input, expected):
    """Test the /bfhl endpoint with parameterized test cases"""
    response = client.post("/bfhl", json=test_input)
    assert response.status_code == 200
    data = response.json()

    # Check required fields
    assert "is_success" in data
    assert data["is_success"] == True

    # Validate response structure
    for key in [
        "user_id", "email", "roll_number", "odd_numbers",
        "even_numbers", "alphabets", "special_characters",
        "sum", "concat_string"
    ]:
        assert key in data

    # Full comparison with expected result
    assert data == expected


def test_root_endpoint():
    """Test the root endpoint returns 200 status code and expected structure"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()

    # Check for presence of expected keys
    assert "message" in data
    assert "timestamp" in data
    assert "timezone" in data

    # Check specific values
    assert data["message"] == "Hello from FastAPI server!"
    assert data["timezone"] == "IST (Indian Standard Time)"


def test_bfhl_endpoint_case1():
    """Test the /bfhl endpoint with test case 1 data"""
    response = client.post("/bfhl", json=test_data)
    assert response.status_code == 200
    data = response.json()

    # Check that the response has all required fields
    assert "is_success" in data
    assert "user_id" in data
    assert "email" in data
    assert "roll_number" in data
    assert "odd_numbers" in data
    assert "even_numbers" in data
    assert "alphabets" in data
    assert "special_characters" in data
    assert "sum" in data
    assert "concat_string" in data

    # Print actual result for comparison (useful for first run)
    print("\nActual result from API (Test Case 1):")
    import json
    print(json.dumps(data, indent=4))

    # Basic validation
    assert data["is_success"] == True
    assert isinstance(data["odd_numbers"], list)
    assert isinstance(data["even_numbers"], list)
    assert isinstance(data["alphabets"], list)
    assert isinstance(data["special_characters"], list)

    # Full comparison with expected result
    assert data == expected_result


def test_bfhl_endpoint_case2():
    """Test the /bfhl endpoint with test case 2 data"""
    response = client.post("/bfhl", json=test_data_2)
    assert response.status_code == 200
    data = response.json()

    # Check that the response has all required fields
    assert "is_success" in data
    assert "user_id" in data
    assert "email" in data
    assert "roll_number" in data
    assert "odd_numbers" in data
    assert "even_numbers" in data
    assert "alphabets" in data
    assert "special_characters" in data
    assert "sum" in data
    assert "concat_string" in data

    # Print actual result for comparison (useful for first run)
    print("\nActual result from API (Test Case 2):")
    import json
    print(json.dumps(data, indent=4))

    # Basic validation
    assert data["is_success"] == True
    assert isinstance(data["odd_numbers"], list)
    assert isinstance(data["even_numbers"], list)
    assert isinstance(data["alphabets"], list)
    assert isinstance(data["special_characters"], list)

    # Full comparison with expected result
    assert data == expected_result_2


def test_bfhl_endpoint_case3():
    """Test the /bfhl endpoint with test case 3 data"""
    response = client.post("/bfhl", json=test_data_3)
    assert response.status_code == 200
    data = response.json()

    # Check that the response has all required fields
    assert "is_success" in data
    assert "user_id" in data
    assert "email" in data
    assert "roll_number" in data
    assert "odd_numbers" in data
    assert "even_numbers" in data
    assert "alphabets" in data
    assert "special_characters" in data
    assert "sum" in data
    assert "concat_string" in data

    # Print actual result for comparison (useful for first run)
    print("\nActual result from API (Test Case 3):")
    import json
    print(json.dumps(data, indent=4))

    # Basic validation
    assert data["is_success"] == True
    assert isinstance(data["odd_numbers"], list)
    assert isinstance(data["even_numbers"], list)
    assert isinstance(data["alphabets"], list)
    assert isinstance(data["special_characters"], list)

    # Full comparison with expected result
    assert data == expected_result_3
