'''
https://www.rabbitmq.com/stomp.html


'''
import sys
sys.path.append('..')
import time
import sys
import json
import stomp
from configure_rabbitmq import host



def connect_and_subscribe(conn):
    conn.connect('guest', 'guest', wait=True)
    conn.subscribe(destination='/queue/test', ack='auto')

class MyTestListener(stomp.ConnectionListener):
    def __init__(self, conn):
        self.conn = conn

    def on_connected(self, body):
        #print(f'on_connected {headers} {body}')
        print('on_connected')

    def on_error(self, body):
        print('received an error "%s"' % body)

    def on_message(self, headers, body):
        print('received a message "%s"' % body)
        #self.conn.send(body=json.dumps({'symbol': 'APPL', 'value': 124.12}), destination='/queue/snapshot')

    def on_disconnected(self):
        print('on_disconnected')
        #connect_and_subscribe(self.conn)

# class MyTestListener2(stomp.ConnectionListener):
#     def on_error(self, headers, body):
#         print('received an error "%s"' % body)

#     def on_message(self, headers, body):
#         print('received a message "%s"' % body)


#print('A')
conn = stomp.Connection([(host, 61613)])
#print('B')
conn.set_listener('/amq/queue/mystream_pika', MyTestListener(conn))
#conn.set_listener('/1/message', MyTestListener2())
conn.connect('guest', 'guest', wait=True)
#connect_and_subscribe(conn)
conn.subscribe(destination='/amq/queue/mystream_pika', id=4, ack='client')
#print('here')
#conn.subscribe(destination='/queue/test', id=1, ack='auto')
#print(sys.argv[1:])
#conn.send(body=' '.join(sys.argv[1:]), destination='/queue/test')
#time.sleep(2)
#conn.disconnect()

print('test stomp connected')


while True:
    pass
