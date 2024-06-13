from datetime import datetime
from dotenv import dotenv_values
from elasticsearch import Elasticsearch

class ElasticsearchService:
    def __init__(self, host="http://localhost", port=9200, api_key=dotenv_values(".env")["ELASTIC_API_KEY"]):
        self.client = Elasticsearch(f"{host}:{port}")

    def reindex(self, index, body):
        self.client.indices.delete(index=index, ignore=[400, 404])
        self.client.indices.create(index=index)
        for id, doc in body.items():
            self.index(index=index, id=id, body=doc)

    def index(self, index, id, body):
        return self.client.index(index=index, id=id, body=body)

    def get(self, index, id):
        return self.client.get(index=index, id=id)
    
    def update(self, index, id, body):
        return self.client.update(index=index, id=id, body={"doc": body})
    
    def delete(self, index, id):
        return self.client.delete(index=index, id=id)

    def search(self, index, query):
        resp = self.client.search(index=index, body={"query": query})
        print("RESP:", resp)
        return [hit['_source'] for hit in resp["hits"]["hits"]]

