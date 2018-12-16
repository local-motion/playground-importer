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

if len(sys.argv) != 2:
    logging.info("Usage: python {} $(pwd)/samples/1_playground.csv".format(Path(__file__).name))
    logging.info("""Environment variables to consider, and please note .env file is supported:
    
    # JWT Token
    ID_TOKEN=

    # Local Motion's playground API
    ONBOARDING_API=http://localhost:8082/playgrounds

    # For de-activating TLS certificate validation
    DISABLE_CERTIFICATE_VALIDATION = true

    # Optional, Sentry.io configuration
    SENTRY_DSN=<sentry-dsn>
    
    # Toggles verbose output
    DEBUG=true
    """)
    sys.exit(1)


def configure_http_logging():
    http_client.HTTPConnection.debuglevel = 1

    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG if debug_mode else logging.INFO)
    requests_log.propagate = True


source = sys.argv[1]
jwt_token = os.getenv('ID_TOKEN')

if not jwt_token:
    logging.error("Environment variable ID_TOKEN is required. Consider adding it to your .env file.")
    sys.exit(1)

logging.info("CSV source file: {}".format(source))

if __name__ == '__main__':
    playground_importer = PlaygroundImporter(source, jwt_token)
    playground_importer.parse_playgrounds()

