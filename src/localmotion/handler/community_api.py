import logging

import jsonpickle as jsonpickle
import requests

from src.localmotion.domain.result import Result
from src.localmotion.domain.playground import Playground


class CommunityApi:

    def __init__(self, namespace: str, target_endpoint: str) -> None:
        self.namespace = namespace
        self.target_endpoint = target_endpoint

    def create_or_update(self, playground: Playground):
        try:
            json = jsonpickle.encode(playground, unpicklable=False)
            r = requests.post(self.target_endpoint, data=json)
            logging.info(r)
            if 200 <= r.status_code < 300:
                Result.success(playground, "Added playground {} to Local Motion".format(playground.name))
            else:
                return Result.failure(playground, "Status {}".format(r.status_code))
        except BaseException as e:
            failure_message = "Could not add playground {} to Local Motion at {}".format(
                playground.name, self.target_endpoint)
            return Result.exception(playground, failure_message, e)

