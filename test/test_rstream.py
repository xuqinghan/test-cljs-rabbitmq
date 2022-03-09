'''
python版本 3.9+ 才支持

'''
import asyncio
from rstream import Producer, AMQPMessage

async def publish():
    async with Producer('localhost', username='guest', password='guest') as producer:
        await producer.create_stream('mystream', exists_ok=True)

        for i in range(100):
            amqp_message = AMQPMessage(
                body='hello: {}'.format(i),
            )
            #msg = f'hello: {i}'
            await producer.publish('mystream', amqp_message)

asyncio.run(publish())