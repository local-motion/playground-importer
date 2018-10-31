import logging
import os
import sys
import http.client as http_client

from src.localmotion.playground_importer import PlaygroundImporter
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(verbose=True, override=True)
debug_mode = os.getenv('DEBUG')

# Initialize logging
logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG if debug_mode else logging.INFO)

if len(sys.argv) != 3:
    logging.info("Usage: python {} $(whoami) $(pwd)/samples/1_playground.csv".format(Path(__file__).name))
    logging.info("""Environment variables to consider:
    
    ONBOARDING_API=http://localhost:8082/playgrounds
    SENTRY_DSN=<sentry-dsn>
    DEBUG=true
    """)
    sys.exit(1)


def configure_http_logging():
    http_client.HTTPConnection.debuglevel = 1

    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG if debug_mode else logging.INFO)
    requests_log.propagate = True


namespace = sys.argv[1]
source = sys.argv[2]

logging.info("Namespacing everything in: {}".format(namespace))
logging.info("CSV source file: {}".format(source))

if __name__ == '__main__':
    playground_importer = PlaygroundImporter(namespace, source)
    playground_importer.parse_playgrounds()

