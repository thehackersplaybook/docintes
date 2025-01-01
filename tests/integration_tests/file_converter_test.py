import pytest
from httpx import AsyncClient
from app.main import app  # Replace with your actual module name
from httpx import ASGITransport

@pytest.mark.asyncio
async def test_convert_file_for_valid_file():
    transport = ASGITransport(app=app)
    # Create a test client
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        # Simulate a file upload with valid content
        file_content = b"This is a sample text content for conversion."  # Content must be bytes
        file_data = {
            "uploaded_file": ("test.txt", file_content, "text/plain")  # Filename, content, and MIME type
        }
        # Make a POST request to the /convert endpoint
        response = await client.post("/convert-to-markdown/", files=file_data)

        # Assert the response
        assert response.status_code == 200
        # Assert the response content
        response_data = response.json()
        assert "markdown" in response_data  # Check if the key exists
        expected_markdown = "This is a sample text content for conversion."
        assert response_data["markdown"] == expected_markdown  # Compare content


@pytest.mark.asyncio
async def test_endpoint_when_no_file_provided_in_request():
    transport = ASGITransport(app=app)
    # Create a test client
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        # Make a POST request to the /convert endpoint
        response = await client.post("/convert-to-markdown/")
        # Assert the response for an error
        assert response.status_code == 422
