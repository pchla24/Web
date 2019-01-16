import sys, os, json
import pika

exchange = 'sawickij'
queue = 'sawickij-direct'
routing_key = 'sawickij-thumbs'

print("%s --[%s]--> %s" % (exchange, routing_key, queue))
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue=queue, durable=True)
channel.queue_bind(queue=queue, exchange=exchange, routing_key=routing_key)

def callback(ch, method, properties, body):
    msg_json = body.decode("utf-8")
    print("Recieved {}".format(msg_json))
    msg = json.loads(msg_json)
    os.system("convert -resize 64x64! {} {}".format(msg['userpath']+msg['filename'],
    "/home/sawickij/www/thumbnails/"+msg['user_id']+'/'+msg['filename']))
    channel.basic_ack(delivery_tag=method.delivery_tag)

#channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue=queue,
                      no_ack=False)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()