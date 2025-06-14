from elasticsearch import (
    Elasticsearch
)

from app.db.models import (
    Questions,
    Tests
)

from elasticsearch.exceptions import ConnectionError as ElasticConnectionError
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# elastic_search = Elasticsearch("http://127.0.0.1:9200")

class QuestionSearcher:
    def __init__(self, elastic_search_url: str = "http://127.0.0.1:9200"):
        self.elastic_search = Elasticsearch(elastic_search_url)

    def index_question(self, question: Questions):
        print("ПОЧАТОК ІНДЕКСАЦІЇ ✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅")
        try:
            document = {
                "id": question.id,
                "title": question.title,
                "description": question.description,
                "user_id": question.user_id,
                "status": question.status.value,
            }

            response = self.elastic_search.index(
                index="questions",
                id=question.id,
                document=document
            )

            print("КІНЕЦЬ ІНДЕКСАЦІЇ ✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅")


            logger.info(f"✅ Document indexed: {response}")

        except ElasticConnectionError as e:
            logger.error(f"Connection Error {e}")

    def search_question_elastic(self, query: str):
        try:
            search_response = self.elastic_search.search(
                index =  "questions",
                query = {
                    "multi_match": {
                        "query": query,
                        "fields": ["title", "description"]
                    }
                }
            )

            hits = search_response["hits"]["hits"]

            return [hit["_source"] for hit in hits]
        
        except ElasticConnectionError as e:
            logger.error(f"Connection Error {e}")
            return []


class SearcherTests:
    def __init__(self, elastic_search_url: str = "http://127.0.0.1:9200"):
        self.elastic_search = Elasticsearch(elastic_search_url)

    def index_tests(self, test: Tests):
        print("ПОЧАТОК ІНДЕКСАЦІЇ ✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅")
        try:
            document = {
                "id": test.id,
                "title": test.title,
                "description": test.description,
                "user_id": test.user_id
            }

            response = self.elastic_search.index(
                index="tests",
                id=test.id,
                document=document
            )

            logger.info(f"✅ Document indexed: {response}")

            print("КІНЕЦЬ ІНДЕКСАЦІЇ ✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅")


        except ElasticConnectionError as e:
            logger.error(f"Connection Error {e}")

    def search_tests_elastic(self, query:str):
        try:
            search_response = self.elastic_search.search(
                index="tests",
                query={
                    "multi_match": {
                        "query": query,
                        "fields": ["title", "description"]
                    }
                }
            )

            hits = search_response["hits"]["hits"]

            return [hit["_source"] for hit in hits]
        
        except ElasticConnectionError as e:
            logger.error(f"Connection Error {e}")
            return []