import logging

import jsonpickle as jsonpickle
import requests

from src.localmotion.domain.result import Result
from src.localmotion.domain.playground import Playground


class OnboardingApi:

    def __init__(self, target_endpoint: str, jwt_token: str) -> None:
        self.target_endpoint = target_endpoint
        self.jwt_token = jwt_token

    def create_or_update(self, playground: Playground):
        try:
            json = jsonpickle.encode(playground, unpicklable=False)
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.jwt_token)
            }
            r = requests.post(self.target_endpoint, headers=headers, data=json)
            logging.info(r)
            if 200 <= r.status_code < 300:
                return Result.success(playground, "Added playground {} to Local Motion".format(playground.name))
            else:
                return Result.failure(playground, "Status {}".format(r.status_code))
        except BaseException as e:
            failure_message = "Could not add playground {} to Local Motion at {}".format(
                playground.name, self.target_endpoint)
            return Result.exception(playground, failure_message, e)

