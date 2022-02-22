from datetime import datetime
from elasticsearch import Elasticsearch
import os
from dotenv import load_dotenv
load_dotenv()

elasticHost = os.environ['elasticHost']
elasticUser = os.environ['elasticUser']
elasticPassword = os.environ['elasticPassword']

es = Elasticsearch([elasticHost], http_auth=(elasticUser, elasticPassword))


doc = {
    'author': 'kimchy2',
    'text': 'Elasticsearch: cool. bonsai cool.',
    'timestamp': datetime.now(),
}
res = es.index(index="insightdata", id=1, document=doc)
print(res['result'])

res = es.get(index="insightdata", id=1)
print(res['_source'])

es.indices.refresh(index="insightdata")

res = es.search(index="insightdata", query={"match_all": {}})
print("Got %d Hits:" % res['hits']['total']['value'])
for hit in res['hits']['hits']:
    print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])