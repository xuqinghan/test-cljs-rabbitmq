'''
基本假设gm永远在线,客户端频繁上下线
'''
#import os
import subprocess
import json
import shlex
import pika
import sys
from pathlib import Path

host = 'localhost'

para_connection = pika.ConnectionParameters(
                        host=host,
                        #heartbeat_interval=600,
                        blocked_connection_timeout=10000)



def define(channel):

    #stream
    queue = channel.queue_declare(queue='mystream_pika', 
        durable = True,
        exclusive = False,
        auto_delete = False, # not exclusive, not auto-delete
        arguments = {"x-queue-type": "stream"}
        )
    queue_name = queue.method.queue
    print('queue_name ', queue_name)

    channel.exchange_declare(exchange='stream_ex',
                             exchange_type='direct')

    channel.queue_bind(exchange='stream_ex',
                       queue=queue_name,
                       routing_key=queue_name)




def publish(channel):
    for i in range(100):
        msg = f'hello: {i}'
        channel.basic_publish('stream_ex', routing_key='mystream_pika', body=msg)

# def recv(channel):
#     def on_player_prepare_game(ch, method, properties, body):
#         print(f" [x] Received from stream {body}")
#         ch.basic_ack(delivery_tag = method.delivery_tag)

#     channel.basic_qos(prefetch_count=10)
#     channel.basic_consume(queue='mystream_pika', 
#                             on_message_callback=on_player_prepare_game,
#                             auto_ack = False,
#                             exclusive= False,
#                             arguments = {
#                                 "x-stream-offset": "first",
#                                 'durable': True,
#                                 'auto-delete': False,
#                                 'x-queue-type': 'stream',
#                                 }
#                             )
#     channel.start_consuming()




if __name__ == '__main__':
    '''配置rabbitmq'''
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=host))

    channel = connection.channel()

    define(channel)
    publish(channel)
    #recv(channel)
    connection.close()