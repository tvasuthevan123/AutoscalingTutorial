#!/usr/bin/env python
import pika, sys, os, time

from autoscalingtutorial.utils import get_rmq_addr, get_rmq_creds

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

        # Simulate processing delay
        time.sleep(0.2)

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
