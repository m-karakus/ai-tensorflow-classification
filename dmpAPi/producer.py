from kafka import KafkaProducer
from kafka.errors import KafkaError
from time import sleep
from json import dumps
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

elasticHost = os.environ['elasticHost']
elasticUser = os.environ['elasticUser']
elasticPassword = os.environ['elasticPassword']

def main(data):
    producer = KafkaProducer(bootstrap_servers=[elasticHost],
                            value_serializer=lambda x: 
                            dumps(x).encode('utf-8'))

    # Asynchronous by default
    future = producer.send('dmpAPI', key=b'data', value=data)

    # Block for 'synchronous' sends
    record_metadata = future.get(timeout=10)

    # Successful result returns assigned partition and offset
    # print (record_metadata.topic)
    # print (record_metadata.offset)
    return

if __name__ == "__main__":
    data = {"data": {"aglsdajfew": """sdjf'sd\+%:)/sdaf*-1'^57"793é3jf"""}}
    main(data)