from core.utils import megabytes_to_bytes
from django.core.exceptions import ValidationError


def validate_file_less_than_5mb(fileobj):        # validate file size of uploaded image
    filesize = fileobj.file.size
    megabyte_limit = 5.0
    if filesize > megabytes_to_bytes(megabyte_limit):
        raise ValidationError(f'Max file size is {megabyte_limit}MB')
