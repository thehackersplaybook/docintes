# services/file_converter.py
import os
import logging

from markitdown import MarkItDown

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("file_converter")


def convert_file(file_path: str) -> dict[str, str]:
    """
    Converts a file (e.g., PDF) to a markdown representation.
    Args:
        file_path (str): The path to the file to convert.

    Returns:
        str: The converted content in markdown format.
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        # Use MarkItDown to convert the file
        markdown_converter = MarkItDown()
        markdown_content = markdown_converter.convert(file_path)
        logger.info("Converted file to markdown")

        # Delete the file after processing (optional, to keep the server clean)
        os.remove(file_path)
        logger.info("remove the temp file")

        # Return the converted markdown content
        logger.info("Returning from file_converter")
        return {"status": "success", "markdown": markdown_content.text_content}
    except Exception as e:
        raise Exception(f"Error during file conversion: {str(e)}")


