# this is a client to hammer API endpoints for test purposes

import argparse
import dotenv
import logging
import urllib3.exceptions
from datetime import datetime, timedelta, timezone
#from multiprocessing import Process, Pool
from threading import Thread

from swagger_client.api_client import ApiClient
from swagger_client.configuration import Configuration
from swagger_client.api.sshkeys_api import SshkeysApi
import swagger_client.rest

TSFORMAT = "%Y-%m-%d %H:%M:%S%z"


def call_uis(ssh_api, secret, tst):

    # call the api
    uis_keys = list()
    try:
        uis_keys = ssh_api.bastionkeys_get(secret=secret, since_date=tst)
    except urllib3.exceptions.MaxRetryError:
        logger.error(f'Unable to contact UIS/Core API at {dotconfig["UIS_HOST_URL"]}, continuing')
    except swagger_client.rest.ApiException as e:
        logger.error(f'UIS returned API error {e}')

    print(f'Retrieved keys for {uis_keys=}')


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--config", action="store",
                        help="Alternative name of config .env file. "
                        )

    parser.add_argument("-t", "--threads", action="store", default="1",
                        help="Number of parallel threads to spawn")

    args = parser.parse_args()

    # massage the config with defaults
    dotconfig = dotenv.dotenv_values(args.config)
    if not dotconfig.get("LOG_FILE"):
        dotconfig["LOG_FILE"] = 'stdout'
    if not dotconfig.get("UIS_HOST_URL"):
        dotconfig["UIS_HOST_URL"] = "https://127.0.0.1:8443/"

    logging.basicConfig()
    logger = logging.getLogger('bastion-key-client')

    # prepare API client
    config = Configuration()
    config.host = dotconfig["UIS_HOST_URL"]
    config.verify_ssl = True if dotconfig.get("UIS_HOST_SSL_VALIDATE", "True") == "True" else False

    api_client = ApiClient(config)
    ssh_api = SshkeysApi(api_client)

    now = datetime.now(timezone.utc)
    delta = timedelta(minutes=600)
    check_instant = now - delta
    logger.debug(f'{check_instant.tzname()}')
    ts = check_instant.strftime(TSFORMAT)

    print(f'Starting {args.threads} threads')
    for i in range(0, int(args.threads)):
        p = Thread(target=call_uis, args=(ssh_api, dotconfig["UIS_API_SECRET"], ts))
        p.start()
        p.join()

    print('Done')