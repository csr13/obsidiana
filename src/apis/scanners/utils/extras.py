from base64 import b64encode
from pathlib import Path



def convert_file_to_base64(file: str):
    """convert file to base64 bytes"""
    with open(file, mode="rb") as f:
        bytes_file = f.read()
        encode_string = b64encode(bytes_file)
    return encode_string


def sanitize_host(host: str):
    """remove ., :, /, // if exist in host"""
    if '.' in host:
        host = ''.join(host.split('.'))
    if ':' in host:
        host = ''.join(host.split(':'))
    if '/' in host:
        host = ''.join(host.split('/'))
    if '//' in host:
        host = ''.join(host.split('//'))
    return host
