#!/usr/bin/env python
import pika, sys, os, time

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

def main():
    host = get_rmq_addr()
    user, password = get_rmq_creds()

    credentials = pika.PlainCredentials(user, password)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=host.strip(), 
            credentials=credentials
        )
    )

    channel = connection.channel()

    channel.queue_declare(queue='hello')

    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")
        time.sleep(5)

    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming() 


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
