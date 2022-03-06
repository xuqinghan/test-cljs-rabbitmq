import sys
sys.append('..')
import time
import sys
import json
import stomp
from configure_rabbitmq import host



def connect_and_subscribe(conn):
    conn.connect('guest', 'guest', wait=True)
    conn.subscribe(destination='/queue/test', id=1, ack='auto')

class MyTestListener(stomp.ConnectionListener):
    def __init__(self, conn):
        self.conn = conn

    def on_connected(self, headers, body):
        print(f'on_connected {headers} {body}')


    def on_error(self, headers, body):
        print('received an error "%s"' % body)

    def on_message(self, headers, body):
        print('received a message "%s"' % body)
        self.conn.send(body=json.dumps({'symbol': 'APPL', 'value': 124.12}), destination='/queue/wg_logs')

    def on_disconnected(self):
        print('on_disconnected')
        connect_and_subscribe(self.conn)

# class MyTestListener2(stomp.ConnectionListener):
#     def on_error(self, headers, body):
#         print('received an error "%s"' % body)

#     def on_message(self, headers, body):
#         print('received a message "%s"' % body)


#print('A')
conn = stomp.Connection([(host, 61613)])
#print('B')
conn.set_listener('/queue/test', MyTestListener(conn))
#conn.set_listener('/1/message', MyTestListener2())
#conn.connect('guest', 'guest', wait=True)
connect_and_subscribe(conn)
#print('here')
#conn.subscribe(destination='/queue/test', id=1, ack='auto')
print(sys.argv[1:])
conn.send(body=' '.join(sys.argv[1:]), destination='/queue/test')
#time.sleep(2)
#conn.disconnect()
while True:
    pass
