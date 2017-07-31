import os
from django.core.exceptions import ValidationError
from kompose_ui import settings
import logging

# Get logger instance
logger = logging.getLogger('default')


def validate_file_extension(file):
    """
    Checks extension of the uploaded file
    :param file: Uploaded file

    Raises Validation Error if file extension is not listed in settings.py under ALLOWED_EXTENSIONS
    Raises Validation Error if file size is greater than MAX_FILE_SIZE in settings.py
    """
    # Check for valid extensions
    ext = os.path.splitext(file.name)[1]
    valid_extensions = settings.ALLOWED_EXTENSIONS
    if not ext.lower() in valid_extensions:
        error = 'Unsupported file extension {0}.'.format(ext)
        raise ValidationError(error)

    # Check for valid file size set in settings.py
    if file.size > settings.MAX_FILE_SIZE * 1024 * 1024:
        error = "File too large. Allowed Size: {0}. Uploaded Size: {1}".format(settings.MAX_FILE_SIZE, file.size)
        raise ValidationError(error)
