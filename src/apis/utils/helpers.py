import uuid


def generate_output_location(username, scanner_name):
    return "%s_%s_%s" % (
        username.lower(), 
        scanner_name.lower(),
        uuid.uuid4().hex
    )


