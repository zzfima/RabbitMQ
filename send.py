import time
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5673))
channel = connection.channel()

channel.exchange_declare(exchange='timestamps', exchange_type='fanout')

while True:
    time.sleep(2)
    body_to_send = 'Hello World!' + ' ' + str(time.time())
    channel.basic_publish(exchange='timestamps', routing_key='', body=body_to_send)

connection.close()
