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
import atexit

import dotenv
import logging
import os
from datetime import datetime, timedelta, timezone

import urllib3.exceptions
from filelock import FileLock, Timeout
import ansible_runner

from bastion_key_client.bastion_ansible import BastionAnsibleUserList
from bastion_key_client.bastion_homedir import HomedirScanner

from swagger_client.api_client import ApiClient
from swagger_client.configuration import Configuration
from swagger_client.api.sshkeys_api import SshkeysApi

TSFORMAT = "%Y-%m-%d %H:%M:%S%z"

lock = None
logger = None


@atexit.register
def exit_handler():
    if lock:
        lock.release()
    else:
        if not logger:
            logger.warning("No lock was acquired. Exiting.")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--config", action="store",
                        help="Alternative name of config .env file. See README.md"
                        )
    parser.add_argument("-d", "--debug", action="count",
                        help="Turn on debugging")
    parser.add_argument("-t", "--test", action="count",
                        help="Do not execute the playbook, simply collect the playbook extra variables in a file.")

    args = parser.parse_args()


    # massage the config with defaults
    dotconfig = dotenv.dotenv_values(args.config)
    if not dotconfig.get("LOG_FILE"):
        dotconfig["LOG_FILE"] = 'stdout'
    if not dotconfig.get("TIMESTAMP_FILE"):
        dotconfig["TIMESTAMP_FILE"] = "/tmp/bastion-timestamp"
    if not dotconfig.get("UIS_HOST_URL"):
        dotconfig["UIS_HOST_URL"] = "https://127.0.0.1:8443/"
    if not dotconfig.get("BACKOFF_PERIOD"):
        dotconfig["BACKOFF_PERIOD"] = "1440"  # one day
    if not dotconfig.get("HOME_PREFIX"):
        dotconfig["HOME_PREFIX"] = "/home"
    if not dotconfig.get("LOCK_FILE"):
        dotconfig["LOCK_FILE"] = "/tmp/bastion-timestamp.lock"
    if not dotconfig.get("EXTRA_VARS_FILE"):
        dotconfig["EXTRA_VARS_FILE"] = "/tmp/bastion-users.json"

    logging.basicConfig()
    logger = logging.getLogger('bastion-key-client')
    if args.debug is None:
        # quiet all loggers
        loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
        for logger in loggers:
            logger.setLevel(logging.ERROR)
        logger.setLevel(logging.INFO)
        # configure our logger
        if dotconfig["LOG_FILE"] == 'stdout':
            handler = logging.StreamHandler(sys.stdout)
        else:
            handler = logging.FileHandler(filename=dotconfig["LOG_FILE"], encoding='utf-8')
        handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - {%(filename)s:%(lineno)d} - '
                                               '[%(threadName)s] - %(levelname)s - %(message)s'))
        logger.addHandler(handler)
    elif args.debug >= 1:
        # dump everything to stdout
        logger.setLevel(logging.DEBUG)

    if not dotconfig.get("UIS_API_SECRET"):
        logger.error(f".env configuration file must specify UIS_API_SECRET. "
                      f"Update configuration and try again. Exiting")
        sys.exit(-1)

    if not dotconfig.get("EXCLUDE_LIST_FILE"):
        logger.error(f".env configuration file must specify EXCLUDE_LIST_FILE. "
                      f"Update configuration and try again. Exiting")

    # lock
    lock = FileLock(dotconfig["LOCK_FILE"], 0)
    logger.info("Acquiring lock file (trying at most for 5 seconds)")
    try:
        lock.acquire(timeout=5)
    except Timeout:
        logger.error(f"Unable to acquire file lock, another instance is likely executing. If you are sure,"
                      f" remove file {dotconfig['LOCK_FILE']} and try again. Exiting.")
        sys.exit(-2)

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
        logger.debug(f'{check_instant.tzname()}')
        ts = check_instant.strftime(TSFORMAT)

    # update timestamp
    with open(dotconfig["TIMESTAMP_FILE"], "w", encoding='utf8') as f:
        now = datetime.now(timezone.utc)
        f.write(now.strftime(TSFORMAT))

    logger.info(f'Using time {ts} to query UIS/CoreAPI (now is {now.strftime(TSFORMAT)})')

    # prepare API client
    config = Configuration()
    config.host = dotconfig["UIS_HOST_URL"]
    config.verify_ssl = True if dotconfig.get("UIS_HOST_SSL_VALIDATE", "True") == "True" else False

    api_client = ApiClient(config)
    ssh_api = SshkeysApi(api_client)

    # call the api
    uis_keys = list()
    try:
        uis_keys = ssh_api.bastionkeys_get(secret=dotconfig["UIS_API_SECRET"], since_date=ts)
    except urllib3.exceptions.MaxRetryError:
        logger.error(f'Unable to contact UIS/Core API at {dotconfig["UIS_HOST_URL"]}, continuing')

    # populate initially
    userlist = BastionAnsibleUserList(uis_keys)

    logger.debug(f'Account and key list after talking to UIS: {userlist}')

    # scan home directories
    exclude_list = list()
    logger.debug(f'Reading exclude list from {dotconfig["EXCLUDE_LIST_FILE"]}')
    with open(dotconfig['EXCLUDE_LIST_FILE'], 'r', encoding='utf-8') as f:
        list_from_file = f.read()
    exclude_list = list_from_file.split()

    # prejudice governs whether keys that don't have expiration date comments on them
    # get blown away (prejudice==True) or are left alone (prejudice==False)
    prejudice = True if dotconfig.get("WITH_PREJUDICE", "False") == "True" else False
    logger.debug(f'Preparing to scan {dotconfig["HOME_PREFIX"]} for users keys. Using prejudice setting {prejudice}')
    home_scanner = HomedirScanner(exclude_list,
                                  dotconfig["HOME_PREFIX"], prejudice)
    for key in home_scanner.scan():
        userlist.add_key(key)

    logger.debug(f'Account and key list after scanning home directories {userlist}')

    if userlist.usercount > 0:
        # save to JSON extra vars file
        logger.info(f'Saving account and key information to extra vars file {dotconfig["EXTRA_VARS_FILE"]}')
        with open(dotconfig['EXTRA_VARS_FILE'], 'w', encoding='utf-8') as f:
            f.write(userlist.to_json())
        if args.test is None:
            logger.info(f'Executing Ansible role for the following users: {userlist.usernames} (keys added or removed)')
            # make sure our ansible cfg is respected
            os.environ["ANSIBLE_CONFIG"] = os.path.join(BastionAnsibleUserList.get_package_path(),
                                                        'ansible', 'fabric-bastion', 'ansible.cfg')
            out, err, rc = ansible_runner.run_command(
                executable_cmd='ansible-playbook',
                # somewhat NOT platform-independent
                cmdline_args=[os.path.join(BastionAnsibleUserList.get_package_path(), 'ansible',
                                           'fabric-bastion', 'site.yml'),
                              '--tags', 'user-experimenter-dynamic',
                              '--extra-vars', '@' + dotconfig['EXTRA_VARS_FILE']],
                input_fd=sys.stdin,
                output_fd=sys.stdout,
                error_fd=sys.stderr,
            )
            logger.info(f'Ansible playbook exited with status {rc}, deleting extra vars file.')
            os.remove(dotconfig["EXTRA_VARS_FILE"])
        else:
            logger.info(f'Running in test mode, ansible role will not be executed, extra vars file is preserved.')
    else:
        logger.info(f'No user keys added or removed, exiting')


