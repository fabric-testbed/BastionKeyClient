#!/usr/bin/env python3
# MIT License
#
# Copyright (c) 2020 FABRIC Testbed
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
#
# Author: Ilya Baldin (ibaldin@renci.org)

import argparse
import sys

import dotenv
import logging
import os
from datetime import datetime, timedelta, timezone

from bastion_key_client.bastion_ansible import BastionAnsibleUserList
from bastion_key_client.bastion_homedir import HomedirScanner

from swagger_client.api_client import ApiClient
from swagger_client.configuration import Configuration
from swagger_client.api.sshkeys_api import SshkeysApi

TSFORMAT = "%Y-%m-%d %H:%M:%S%z"

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--config", action="store",
                        help="Alternative name of config .env file. See README.md"
                        )
    parser.add_argument("-d", "--debug", action="count",
                        help="Turn on debugging")

    args = parser.parse_args()

    if args.debug is None:
        logging.basicConfig(level=logging.INFO)
    elif args.debug >= 1:
        logging.basicConfig(level=logging.DEBUG)

    # massage the config with defaults
    dotconfig = dotenv.dotenv_values(args.config)
    if not dotconfig.get("TIMESTAMP_FILE"):
        dotconfig["TIMESTAMP_FILE"] = "/tmp/bastion-timestamp"
    if not dotconfig.get("UIS_HOST_URL"):
        dotconfig["UIS_HOST_URL"] = "https://127.0.0.1:8443/"
    if not dotconfig.get("BACKOFF_PERIOD"):
        dotconfig["BACKOFF_PERIOD"] = "1440"  # one day
    if not dotconfig.get("HOME_PREFIX"):
        dotconfig["HOME_PREFIX"] = "/home"
    if not dotconfig.get("UIS_API_SECRET"):
        print(f".env configuration file must specify UIS_API_SECRET")
        sys.exit(-1)

    # figure out how far to go back in time
    if os.path.isfile(dotconfig["TIMESTAMP_FILE"]):
        # read timestamp
        with open(dotconfig["TIMESTAMP_FILE"], "r", encoding="utf8") as f:
            ts = f.read()
    else:
        # use backoff period
        now = datetime.now(timezone.utc)
        delta = timedelta(minutes=int(dotconfig["BACKOFF_PERIOD"]))
        check_instant = now - delta
        logging.debug(f'{check_instant.tzname()}')
        ts = check_instant.strftime(TSFORMAT)

    # update timestamp
    with open(dotconfig["TIMESTAMP_FILE"], "w", encoding='utf8') as f:
        now = datetime.now(timezone.utc)
        f.write(now.strftime(TSFORMAT))

    logging.debug(f'Using time {ts} to query UIS/CoreAPI (now is {now.strftime(TSFORMAT)})')

    # prepare API client
    config = Configuration()
    config.host = dotconfig.get("UIS_HOST_URL", "https://127.0.0.1:8443/")
    config.verify_ssl = True if dotconfig.get("UIS_HOST_SSL_VALIDATE", "True") == "True" else False

    api_client = ApiClient(config)
    ssh_api = SshkeysApi(api_client)

    # call the api
    uis_keys = ssh_api.bastionkeys_get(secret=dotconfig["UIS_API_SECRET"], since_date=ts)

    # populate initially
    userlist = BastionAnsibleUserList(uis_keys)

    # scan home directories
    exclude_list = list()
    if dotconfig.get('EXCLUDE_LIST_FILE'):
        logging.debug(f'Reading exclude list from {dotconfig["EXCLUDE_LIST_FILE"]}')
        with open(dotconfig['EXCLUDE_LIST_FILE'], 'r', encoding='utf-8') as f:
            list_from_file = f.read()
        exclude_list = list_from_file.split()

    prejudice = True if dotconfig.get("WITH_PREJUDICE", "False") == "True" else False
    logging.debug(f'Preparing to scan {dotconfig["HOME_PREFIX"]} for users keys. Using prejudice setting {prejudice}')
    home_scanner = HomedirScanner(exclude_list,
                                  dotconfig["HOME_PREFIX"], prejudice)
    for key in home_scanner.scan():
        userlist.add_key(key)

    print(userlist.to_json())
