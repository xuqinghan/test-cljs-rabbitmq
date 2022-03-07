'''
基本假设gm永远在线,客户端频繁上下线
'''
import sys
sys.path.append('..')
import pika
from configure_rabbitmq import para_connection
import time
import json
from datetime import datetime

connection = pika.BlockingConnection(para_connection)

channel = connection.channel()

#当前推演是否进行中
states = {'0': '进行中'}

#玩家请求初始化1场退
#queue_prepare_game = channel.queue_declare(queue='', exclusive=True)
#queue_name = queue_prepare_game.method.queue
# channel.queue_bind(exchange='player-request', 
#                     queue=queue_name,
#                     routing_key='prepare_game')
#    channel.queue_bind(exchange='player-request', queue='player-compile-command')
queue_name = 'player-compile-command'

def on_player_prepare_game(ch, method, properties, body):
    '''一个gid的1个玩家要求初始化1个gid'''
    msg = json.loads(body)
    print(" [x] Received on_player_prepare_game %r" % msg)
    # 形如 {'gid': '0', 'role': '1', 'routing_key': 'gid-0-role-1'}
    #gid = msg['gid']
    #print('gid', gid)
    #routing_key = msg['routing_key']
    #print(" [x] Done")
    ch.basic_ack(delivery_tag = method.delivery_tag)
    #1 如果推演进行中，则通知war-runtime，初始化1个gid（是否已经初始化不管了)
    # if states['gid'] == '进行中':
    gid = '111'
    ch.basic_publish(exchange='war-snapshot', routing_key=gid, body=json.dumps({'gid': gid}))

    #2 通知db，初始化1个阵营的前端（gid-role） 如果有前端要求的特定初始化交互步骤，在这里负责！
    #ch.basic_publish(exchange='', routing_key='init_snapshot_player', body=body)


print('gm connected')
channel.basic_consume(queue=queue_name, on_message_callback=on_player_prepare_game)
channel.start_consuming()