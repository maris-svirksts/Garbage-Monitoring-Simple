"""Various helpers for the main class."""

import os
import base64
import re
import pathlib

def set_full_path_to_file(file: str) -> str:
    """Generate a full path to file."""
    return os.path.join(os.path.dirname(__file__), file)

def base64_encode_photo(photo: str) -> str:
    """Get file and transform it to base64 string."""
    if photo:
        with open(set_full_path_to_file(photo), "rb") as image_file:
            return base64.b64encode(image_file.read())
    else:
        return ''

def base64_photo_to_file(base64_string: str, result_file: str) -> None:
    """Decode a base64 string and save to file."""
    with open(set_full_path_to_file(result_file), "wb") as file:
        file.write(base64.decodebytes(base64_string))

def check_word(value: str) -> str:
    """Validate if word contains only alphanumeric characters."""
    regex: str = "^[a-zA-Z]+$"

    if not re.match(regex, value):
        raise ValueError("Non-alphabetic characters are present: ", value)

    return value

def check_if_true(value: bool) -> bool:
    """Raise an error if value doesn't exist."""
    if not value:
        raise ValueError("Admin Flag set to ", value)

    return value

def validate_extension(value: str) -> str:
    """Raise an error if file extension not in the list."""
    file_extension: str = pathlib.Path(value).suffix

    if file_extension not in ['.png', '.jpg', '.jpeg']:
        raise ValueError("Extension not allowed: ", value)

    return value
