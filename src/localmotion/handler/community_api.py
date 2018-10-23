import logging
import requests

from src.localmotion.domain.result import Result
from src.localmotion.domain.playground import Playground


class CommunityApi:

    def __init__(self, namespace: str, target_endpoint: str) -> None:
        self.namespace = namespace
        self.target_endpoint = target_endpoint

    def create_or_update(self, playground: Playground):
        try:
            r = requests.post(self.target_endpoint, data=playground)
            logging.info(r)
            Result.success(playground, "Added playground {} to Local Motion".format(playground.title))
        except BaseException as e:
            failure_message = "Could not add playground {} to Local Motion at {}".format(
                playground.title, self.target_endpoint)
            return Result.failure(playground, failure_message, e)

