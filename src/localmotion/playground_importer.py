import logging
import os
import time
import uuid

import geocoder
import pandas as pd
from joblib import Memory
from raven import Client

from src.localmotion.domain.address import Address
from src.localmotion.domain.geo_location import GeoLocation
from src.localmotion.domain.playground import Playground
from src.localmotion.domain.result import Result
from ..localmotion.handler.onboarding_api import OnboardingApi

location = './cachedir'
memory = Memory(location, verbose=0)


# These two lines enable debugging at httplib level (requests->urllib3->http.client)
# You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
# The only thing missing will be the response.body which is not logged.
try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client
http_client.HTTPConnection.debuglevel = 1

# You must initialize logging, otherwise you'll not see debug output.
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True


class PlaygroundImporter:
    def __init__(self, namespace: str, source: str, jwt_token: str) -> None:
        self.namespace = namespace
        self.source = source
        self.jwt_token = jwt_token
        self.sentry = PlaygroundImporter.__configure_sentry()
        self.community = self.__configure_onboarding_api()

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

    def __configure_onboarding_api(self):
        target_endpoint = os.getenv('ONBOARDING_API')
        if target_endpoint is None:
            logging.warning("You are NOT using Local Motion community API")
            return None
        logging.info("Connecting to Local Motion community API using {}".format(target_endpoint))
        return OnboardingApi(self.namespace, target_endpoint, self.jwt_token)

    def __report_exception(self, msg, *args, **kwargs):
        logging.error(msg, args, kwargs)
        if self.sentry is not None:
            self.sentry.captureException()

    @staticmethod
    def geocode(address: str):
        logging.info("Fetching geolocation for [{}] from LocationIQ".format(address))
        logging.info("Waiting 1 second to avoid rate limiting from LocationIQ")
        time.sleep(1)
        g = geocoder.locationiq(address, key=os.getenv('LOCATIONIQ_API_KEY'))
        return GeoLocation(g.latlng[0], g.latlng[1])

    @staticmethod
    def determine_status(imported_status: str):
        if imported_status == 'Geheel rookvrij':
            return "finished"
        elif imported_status == "Gedeeltelijk rookvrij":
            return "in_progress"
        else:
            return "not_started"

    @staticmethod
    def determine_website(imported_website: str):
        if imported_website == 'nan':
            return None
        else:
            return imported_website

    def parse_playgrounds(self):
        row_callbacks = [
            self.noop_row_handler('Community API') if self.community is None else self.community.create_or_update,
            # self.noop_row_handler('Mailchimp') if self.mailchimp is None else self.mailchimp.create_or_update,
        ]

        results = []
        playgrounds = pd.read_excel(
            self.source,
            header=0,
            skiprows=0,
            dtype=str
        )
        # Titel	Marker type	Adres	Huisnummer	Postcode	Plaats	Soort	Status	Marker website	Kolom1	Kolom2
        for index, row in playgrounds.iterrows():
            try:
                playground_uuid = str(uuid.uuid4())
                name_ = row['Titel']
                type_ = "smokefree"
                status_ = self.determine_status(row['Status'])
                website_ = self.determine_website(row['Marker website'])
                address_ = Address(
                    row['Adres'],
                    row['Huisnummer'],
                    row['Postcode'],
                    row['Plaats']
                )
                readable_address = address_.to_readable_address()

                cached_geocode = memory.cache(func=self.geocode)
                geolocation = cached_geocode(readable_address)
                logging.info("[{}] resulted in {},{}".format(readable_address, geolocation.lat, geolocation.lng))

                playground = Playground(playground_uuid, name_, address_, geolocation, type_, status_, website_)
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
