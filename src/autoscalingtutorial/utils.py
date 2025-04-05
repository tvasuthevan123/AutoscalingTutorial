import os


def get_rmq_addr():
    addr = os.getenv("RMQ_IP")

    if not addr:
        raise Exception("RMQ_IP environment variable not set")

    return addr

def get_rmq_creds():
    user = os.getenv("RMQ_USER")
    password = os.getenv("RMQ_PASS")

    if not user or not password:
        raise Exception("RMQ_USER/RMQ_PASSWORD environment variables not set")

    return user,password
