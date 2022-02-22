import asyncio
from datetime import datetime
from elasticsearch import AsyncElasticsearch
from kafka import KafkaConsumer
import pymssql
import os
import json
from dotenv import load_dotenv
load_dotenv()

server = os.environ['server']
database = os.environ['database']
user = os.environ['user']
password = os.environ['password']
elasticHost = os.environ['elasticHost']
elasticUser = os.environ['elasticUser']
elasticPassword = os.environ['elasticPassword']

async def sqlWrite(doc):
    engine = pymssql.connect(server=server,database=database, user=user,password=password)
    with engine.cursor() as cursor:
        query = f"INSERT INTO insightdata (data) VALUES ('''{doc}''');"
        cursor.execute(query)
        engine.commit()
    engine.close()
    return

async def elasticWrite(doc):
    es = AsyncElasticsearch([elasticHost], http_auth=(elasticUser, elasticPassword))
    # res = await es.index(index="insightdata", id=1, document=doc)
    res = await es.index(index="insightdata", document=doc)
    # print(res['result'])
    await es.indices.refresh(index="insightdata")

    # resp = await es.search(index="insightdata",query={"match_all": {}},size=20,)
    # print(resp['hits']['total'])
    # for hit in resp['hits']['hits']:
    #     print(hit)
    await es.close()
    return

async def main():
    consumer = KafkaConsumer('dmpAPI', bootstrap_servers=[elasticHost],
        group_id='dmpAPI',
        auto_offset_reset = 'earliest',
        value_deserializer=lambda m: json.loads(m)
        )
    for message in consumer:
        # message value and key are raw bytes -- decode if necessary!
        # e.g., for unicode: `message.value`
        # print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition, message.offset, message.key, message.value))
        doc = message.value
        try:
            await elasticWrite(doc)
        except Exception as e:
            # print(e)
            pass
        """
        try:
            await sqlWrite(doc)
        except Exception as e:
            print(e)
            pass
        """
    return 

loop = asyncio.get_event_loop()
loop.run_until_complete(main())