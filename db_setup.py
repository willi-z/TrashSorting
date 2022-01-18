from elasticsearch import Elasticsearch
from elasticsearch.exceptions import RequestError

es = Elasticsearch()

index = "materials"
try:
    print(es.search(index=index, query={"match": {"name": {}}}))
except RequestError:
    es.put_script(index=index, body=dict())
    print("not exist")
