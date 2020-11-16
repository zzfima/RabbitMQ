import pika


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5673))
channel = connection.channel()

channel.exchange_declare(exchange='timestamps', exchange_type='fanout')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='timestamps', queue=queue_name)
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
