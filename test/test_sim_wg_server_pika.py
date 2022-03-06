import sys
sys.append('..')
import pika
from configure_rabbitmq import host
import time
import json


connection = pika.BlockingConnection(para_connection)

channel = connection.channel()


def test_send_wg_logs_to_different_client_via_routing_key():
    '''
        模拟服务器端 1个 pika客户端 而不是stomp客户端
        前置条件:2个浏览器 已经订阅了/exchange/wg-logs/gid-${gid}-role-${role}
        gid-${gid}-role-${role} 是routing_key 
        测试用服务器根据routing_key发送不同消息到2个客户端,是否能接收到
    '''
    #不在这里声明
    # channel.exchange_declare(exchange='wg-logs',
    #                      exchange_type='direct')

    #定时,交替发送
    i = 0
    while True:
        for dst in ['gid-0-role-0', 'gid-0-role-1']:
            msg = {'value': i}
            channel.basic_publish(exchange='wg-logs',
                                  routing_key=dst,
                                  body= json.dumps(msg))
            time.sleep(1)
            i += 1 


def test_online():
    '''#登录
    '''

    # channel.exchange_declare(exchange='player-request',
    #                         exchange_type='direct')

    #online
    online = channel.queue_declare(queue='', exclusive=True)
    queue_name = online.method.queue
    channel.queue_bind(exchange='player-request', 
                        queue=queue_name,
                        routing_key='online')

    def on_player_online(ch, method, properties, body):
        print(" [x] Received %r" % body.decode())
        #time.sleep( body.count('.') )
        #print(" [x] Done")
        ch.basic_ack(delivery_tag = method.delivery_tag)

    channel.basic_consume(queue=queue_name, on_message_callback=on_player_online)

    channel.start_consuming()

if __name__ == '__main__':
    #test_send_wg_logs_to_different_client_via_routing_key()
    test_wt_sync_on_wg_run_time()