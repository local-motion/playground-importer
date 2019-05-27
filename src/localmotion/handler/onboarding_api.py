import logging
import os
import jsonpickle as jsonpickle
import requests

from src.localmotion.domain.result import Result
from src.localmotion.domain.playground import Playground


class OnboardingApi:

    def __init__(self, target_endpoint: str, jwt_token: str) -> None:
        self.target_endpoint = target_endpoint
        self.jwt_token = jwt_token

    def create_or_update(self, playground: Playground):
        certificate_validation_disabled = os.getenv('DISABLE_CERTIFICATE_VALIDATION')

        if certificate_validation_disabled is None or certificate_validation_disabled.upper() != "TRUE":
            verify_certificate = True
        else:
            verify_certificate = False
        logging.info("verify_certificate:" + str(verify_certificate))

        try:
            json = jsonpickle.encode(playground, unpicklable=False)
            headers = {
                "Content-Type": "application/json",
                "AuthBearer": "Bearer {}".format(self.jwt_token)
            }
            r = requests.post(self.target_endpoint, headers=headers, data=json, verify=verify_certificate)
            logging.info(r)
            if 200 <= r.status_code < 300:
                return Result.success(playground, "Added playground {} to Local Motion".format(playground.name))
            else:
                return Result.failure(playground, "Status {}".format(r.status_code))
        except BaseException as e:
            failure_message = "Could not add playground {} to Local Motion at {}".format(
                playground.name, self.target_endpoint)
            return Result.exception(playground, failure_message, e)

