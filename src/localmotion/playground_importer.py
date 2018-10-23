import logging
import os
import uuid

from raven import Client
import pandas as pd

from src.localmotion.domain.address import Address
from src.localmotion.domain.playground import Playground
from src.localmotion.domain.result import Result
from ..localmotion.handler.community_api import CommunityApi


class PlaygroundImporter:
    def __init__(self, namespace: str, source: str) -> None:
        self.namespace = namespace
        self.source = source
        self.sentry = PlaygroundImporter.__configure_sentry()
        self.community = self.__configure_community_api()

    @staticmethod
    def noop_row_handler(subsystem_name):
        return lambda playground: logging.info(
            "{} is disabled and not handling {}".format(subsystem_name, playground.email))

    @staticmethod
    def __configure_sentry():
        sentry_dsn = os.getenv('SENTRY_DSN')
        if sentry_dsn is None:
            logging.warning("You are NOT using Sentry")
            return None
        logging.info("Connecting to Sentry using DSN {}".format(sentry_dsn))
        return Client(sentry_dsn)

    def __configure_community_api(self):
        target_endpoint = os.getenv('COMMUNITY_API')
        if target_endpoint is None:
            logging.warning("You are NOT using Local Motion community API")
            return None
        logging.info("Connecting to Local Motion community API using {}".format(target_endpoint))
        return CommunityApi(self.namespace, target_endpoint)

    def __report_exception(self, msg, *args, **kwargs):
        logging.error(msg, args, kwargs)
        if self.sentry is not None:
            self.sentry.captureException()

    def parse_playgrounds(self):
        row_callbacks = [
            self.noop_row_handler('Community API') if self.community is None else self.community.create_or_update,
            # self.noop_row_handler('Mailchimp') if self.mailchimp is None else self.mailchimp.create_or_update,
        ]

        results = []
        playgrounds = pd.read_excel(
            # '/Users/erik/dev/local-motion/playground-importer/samples/private_14082018rookvrijelocatiesspelen_KDJ.xlsx',
            '/Users/erik/dev/local-motion/playground-importer/samples/1_playground.xlsx',
            header=0,
            skiprows=0
        )
        # Titel	Marker type	Adres	Huisnummer	Postcode	Plaats	Soort	Status	Marker website	Kolom1	Kolom2
        for index, row in playgrounds.iterrows():
            try:
                playground_uuid = str(uuid.uuid4())[:8]
                name_ = row['Titel']
                type_ = row['Soort']
                status_ = row['Status']
                website_ = row['Marker website']
                address_ = Address(
                    row['Adres'],
                    row['Huisnummer'],
                    row['Postcode'],
                    row['Plaats']
                )

                playground = Playground(playground_uuid, name_, address_, type_, status_, website_)
                for row_callback in row_callbacks:
                    result = row_callback(playground) or \
                             Result.general_failure(playground, "Function didn't return a result")
                    results.append(result)
                    result.assign_line_number(index)
            except BaseException as e:
                self.__report_exception("Parsing CSV failed: {}".format(e))

        for result in results:
            if result.is_failure():
                failure_message = "Failed line #{}: {} {}".format(
                    result.line_number, result.message, result.exception)
                logging.error(failure_message)
            else:
                logging.info("Success line #{}: {}".format(result.line_number, result.message))
