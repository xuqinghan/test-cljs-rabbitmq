'''
game-prepare阶段的调度！

接受前端加载1场gid的请求  发起prepare game:
如果有前端要求的特定初始化交互步骤，在这里负责！

所有图层列表


1 根据每场推演的元数据，通知db，初始化1个阵营的前端（gid-role）：
    1 发送snapshot(scenario)
    (发送完snapshot，前端自己决定开始对时，完成wg-logs下载)

2 根据gid是否"进行中"，通知war-runtime加载1场"进行中"的推演(gid).
    1 发送snapshot(scenario)
    2 发送logs

'''
import sys
sys.append('..')
import pika
from configure_rabbitmq import para_connection
import time
import json
from datetime import datetime

connection = pika.BlockingConnection(para_connection)

channel = connection.channel()

#当前推演是否进行中
states = {'0': '进行中'}

#玩家请求初始化1场退役
queue_prepare_game = channel.queue_declare(queue='', exclusive=True)
queue_name = queue_prepare_game.method.queue
channel.queue_bind(exchange='player-request', 
                    queue=queue_name,
                    routing_key='prepare_game')

def on_player_prepare_game(ch, method, properties, body):
    '''一个gid的1个玩家要求初始化1个gid'''
    msg = json.loads(body)
    print(" [x] Received on_player_prepare_game %r" % msg)
    # 形如 {'gid': '0', 'role': '1', 'routing_key': 'gid-0-role-1'}
    gid = msg['gid']
    print('gid', gid)
    routing_key = msg['routing_key']
    #print(" [x] Done")
    ch.basic_ack(delivery_tag = method.delivery_tag)
    #1 如果推演进行中，则通知war-runtime，初始化1个gid（是否已经初始化不管了)
    # if states['gid'] == '进行中':
    #     ch.basic_publish(exchange='war-runtime-prepare', routing_key=gid, body=json.dumps({'gid': gid}))

    #2 通知db，初始化1个阵营的前端（gid-role） 如果有前端要求的特定初始化交互步骤，在这里负责！
    #ch.basic_publish(exchange='', routing_key='init_snapshot_player', body=body)



channel.basic_consume(queue=queue_prepare_game, on_message_callback=on_player_prepare_game)
