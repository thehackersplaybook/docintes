# api/convert.py
import os

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.file_converter import convert_file

router = APIRouter()

test_router = APIRouter()


@router.post("/convert-to-markdown/")
async def convert(uploaded_file: UploadFile = File(...)):
    """
    Endpoint to handle the file upload and conversion request.
    """
    global file_location
    try:
        # Save the uploaded file temporarily
        file_location = f"temp_{uploaded_file.filename}"
        with open(file_location, "wb") as f:
            f.write(await uploaded_file.read())

        # Call the file conversion function from the service layer
        converted_content = convert_file(file_location)

        # Return the converted content as a response
        return converted_content

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")
    finally:
        # Clean up the temporary file after processing
        if os.path.exists(file_location):
            os.remove(file_location)


@test_router.get("/test-only")
async def test_only_endpoint():
    return {"message": "This is a test-only endpoint"}
