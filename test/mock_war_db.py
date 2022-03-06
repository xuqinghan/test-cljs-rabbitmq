'''
模拟db的发送端? 为前端 维护1场推演的当前wt 和当前wg-logs

输入是初始化时, 读取指定位置的全部wg-logs, 前端需要的每个snpashot. runtime产生的记录

runtime如果作为1个端(后端): 也会在初始化1个gid时同样请求snaplshot 和 全部wg-logs(如果有)! 

runtime 维护多个运行中的推演对象(类似大厅中进行中的牌局). 如果推演结束,则删除! 前端重放时不通过runtime!

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

#推演的初始状态
gid_snapshot = {'0': {'layer1': '图层1', 'layer2': '图层2'}}
#推演的记录
gid_records = {'0': [0,1,2,3]}

def get_ti(gid):
    return len(gid_records.get(gid, [])) - 1


#--------------game-prepare阶段---------------------------------
#初始1场推演的全部snapshot!

def on_init_snapshots(ch, method, properties, body):
    msg = json.loads(body)
    print(" [x] on_init_snapshots %r" % msg)
    # 形如 {'gid': '0', 'role': '1', 'routing_key': 'gid-0-role-1'}
    # 或 {'gid': '0',  'routing_key': 'gid-0'}
    gid = msg['gid']
    print('gid', gid)
    routing_key = msg['routing_key']
    ti = get_ti(gid)
    print('ti', ti)
    #time.sleep( body.count('.') )
    #print(" [x] Done")
    ch.basic_ack(delivery_tag = method.delivery_tag)
    #查找当前gid的snapshots
    snapshots = gid_snapshot[gid]
    #目前没有阵营迷雾，全部发送！
    for name, data in snapshots.items():
        ch.basic_publish(exchange='war-snapshot', routing_key=routing_key, body=json.dumps({'name': name, 'data': data}))

channel.basic_consume(queue='init_war-snapshots', on_message_callback=on_init_snapshots)


#--------------gaming阶段--------------------------
#请求对时对时ti_server
# queue_ti_server = channel.queue_declare(queue='', exclusive=True)
# queue_name = queue_ti_server.method.queue
# channel.queue_bind(exchange='player-request', 
#                     queue=queue_name,
#                     routing_key='ti_server')

def on_ti_server(ch, method, properties, body):
    msg = json.loads(body)
    print(" [x] Received %r" % msg)
    # 形如 {'gid': '0', 'role': '1', 'routing_key': 'gid-0-role-1'}
    gid = msg['gid']
    print('gid', gid)
    routing_key = msg['routing_key']
    ti = get_ti(gid)
    print('ti', ti)
    #time.sleep( body.count('.') )
    #print(" [x] Done")
    ch.basic_ack(delivery_tag = method.delivery_tag)
    ch.basic_publish(exchange='ti-server', routing_key=routing_key, body=json.dumps({'ti_server': ti}))

channel.basic_consume(queue='query_ti-server', on_message_callback=on_ti_server)

#前/后端请求同步wg_logs 唯一1个队列！
# queue_ti_server = channel.queue_declare(queue='', exclusive=True)
# queue_name = queue_ti_server.method.queue
# channel.queue_bind(exchange='player-request', 
#                     queue=queue_name,
#                     routing_key='ti-sync')

def on_wg_logs_sync(ch, method, properties, body):
    msg = json.loads(body)
    print(f" [x] {datetime.now()} on_wg_logs_sync {msg}")
    # 形如 { 'gid': 0, 'role': 0, 'routing_key': routing_key, 'ti_local': 0, 'ti_server': 3 }
    gid = msg['gid']
    print('gid', gid)
    routing_key = msg['routing_key']
    #ti_local 加1
    ti_beg = msg['ti_local'] + 1
    ti_end = msg['ti_server'] + 1
    print(ti_beg, ti_end)
    #ti = get_ti(gid)
    records = gid_records.get(gid, [])
    N = len(records)
    print('N', N)
    assert all( ti <= N for ti in [ti_beg, ti_end])
    #print('ti', ti)
    #time.sleep( body.count('.') )
    #print(" [x] Done")
    ch.basic_ack(delivery_tag = method.delivery_tag)
    for ti in range(ti_beg, ti_end):
        record1 = records[ti]
        print('send log1', record1)
        ch.basic_publish(exchange='wg-logs', routing_key=routing_key, body=json.dumps({'ti': ti, 'record': record1}))

#全局1个队列
channel.basic_consume(queue='sync-wg_logs', on_message_callback=on_wg_logs_sync)

#war-runtime 发过来1个推演产生的1个记录
def on_product_record(ch, method, properties, body):
    msg = json.loads(body)
    print(" [x] on_product_record %r" % msg)
    # 形如 { 'gid': 0, 'record': record}
    gid = msg['gid']
    print('gid', gid)
    record = msg['record']
    #只保存! 不推送!
    #读取
    records = gid_records.get(gid, [])
    #追加
    records.append(record)
    #保存
    gid_records[gid] = records

channel.basic_consume(queue='wg-runtime-product-record', on_message_callback=on_product_record)

channel.start_consuming()


