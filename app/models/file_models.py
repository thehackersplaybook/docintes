from pydantic import BaseModel


class FileConversionResponse(BaseModel):
    content: str
