import pika
import json

def callback(ch, method, properties, body):
    data = json.loads(body)
    order_id = data.get('order_id')
    customer_id = data.get('customer_id')
    product_id = data.get('product_id')
    status = data.get('status')

    print(f" [x] Notification sent: Order {order_id} for customer {customer_id} and product {product_id} is now {status}.")


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='notificationQueue')
    channel.basic_consume(queue='notificationQueue', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for notification messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    main()
