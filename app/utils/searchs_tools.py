from elasticsearch import (
    Elasticsearch
)

from app.db.models import (
    Questions
)

from elasticsearch.exceptions import ConnectionError as ElasticConnectionError
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

elastic_searck = Elasticsearch("http://127.0.0.1:9200")

def index_question(question: Questions):
    try:
        document = {
            "id": question.id,
            "title": question.title,
            "description": question.description,
            "user_id": question.user_id,
            "status": question.status.value,
        }

        response = elastic_searck.index(
            index="questions",
            id=question.id,
            document=document
        )

        logger.info(f"✅ Document indexed: {response}")

    except ElasticConnectionError as e:
        logger.error(f"Connection Error {e}")

def search_question_elastic(query: str):
    try:
        search_response = elastic_searck.search(
            index="questions",
            query={
                "multi_match":{
                    "query": query,
                    "fields":["title", "description"]
                }
            }
        )

        hits = search_response["hits"]["hits"]

        logger.info(f"Found {len(hits)} hits for query: {query}")

        return [hit["_source"] for hit in hits]
    
    except ElasticConnectionError as e:
        logger.error(f"Connection Error {e}")
        return []