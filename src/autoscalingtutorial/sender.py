import pika

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

    for i in range(100):
        channel.basic_publish(exchange='', routing_key='hello', body=(body:=f'Hello World {i}'))
        print(f"Sent {body}")

    connection.close()

if __name__=="__main__":
    main()
