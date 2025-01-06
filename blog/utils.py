import uuid

def get_random_code():
    # code = uuid.uuid4() # uuid.UUID tipinde bir veridir.
    # code = str(uuid.uuid4())
    code = str(uuid.uuid4())[:11].replace('-','')
    return code




