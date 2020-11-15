import pika
import time

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

while True:
    time.sleep(2)
    body_to_send = 'Hello World!' + ' ' + str(time.time())
    channel.basic_publish(exchange='', routing_key='hello', body=body_to_send)
print(" [x] Sent 'Hello World!'")
connection.close()
