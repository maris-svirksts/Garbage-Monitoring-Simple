import os
import base64
import re
import pathlib

def set_full_path_to_file(file):
    return os.path.join(os.path.dirname(__file__), file)

def base64_encode_photo(photo):
    if photo:
        with open(set_full_path_to_file(photo), "rb") as image_file:
            return base64.b64encode(image_file.read())
    else:
        return ''

def base64_photo_to_file(base64_string, result_file):
    with open(set_full_path_to_file(result_file), "wb") as file:
        file.write(base64.decodebytes(base64_string))

def check_word(value):
    regex = "^[a-zA-Z]+$"
    if not re.match(regex, value):
        raise ValueError("Non-alphabetic characters are present: ", value)

    return value

def check_if_true(value):
    if not value:
        raise ValueError("Admin Flag set to ", value)

    return value

def validate_extension(value):
    file_extension = pathlib.Path(value).suffix

    if file_extension not in ['.png', '.jpg', '.jpeg']:
        raise ValueError("Extension not allowed: ", value)

    return value