#import os
import subprocess
import json
import shlex
import pika
import sys
from pathlib import Path

host = 'localhost'
#host = '192.168.0.181'

para_connection = pika.ConnectionParameters(
                        host=host,
                        #heartbeat_interval=600,
                        blocked_connection_timeout=10000)

def define():
    '''配置rabbitmq'''
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=host))

    channel = connection.channel()

    #------------定义exchange 发布方--------------------
    #-------------前端输出-------------
    #玩家独有的请求,如上线online
    channel.exchange_declare(exchange='player-request',
                            exchange_type='direct')

    #--------后端裁决结果输出---------------
    # 前后端重建都需要重建env
    channel.exchange_declare(exchange='war-snapshot',
                         exchange_type='direct')


    #--------------定义queue 订阅方--------------------
    #测试cljs发送
    channel.queue_declare(queue='player-compile-command', durable=True)
    #测试cljs接收
    channel.queue_declare(queue='snapshot', durable=True)

    channel.queue_bind(exchange='player-request', queue='player-compile-command')
    channel.queue_bind(exchange='war-snapshot', queue='snapshot')

    connection.close()

if __name__ == '__main__':

    define()
