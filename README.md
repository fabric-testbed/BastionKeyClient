# BastionKeyClient
Client for automatically managing SSH keys in bastion hosts

## Requirements.

Python 3.9+, Ansible 2.11+, Vagrant (for testing)

## Directory Structure and Installation

Drop auto-generated clients from swagger directly here (so they end up in
`python-client-generated` folder). Update `python-client-generated/setup.py`
so it installs as its own separate package. 

Pushing to PyPi is separated for the auto-generated swagger client and for the Bastion Key Client itself. 
To push updated swagger client:
```shell
$ cd python-client-generated
$ rm dist/*
$ python setup.py bdist_wheel
$ twine upload dist/*
```
(when updating swagger client, be sure to preserve/update `python-client-generated/setup.py` as it is not default)

Use `pip install python-client-generated/` for development, otherwise install as dependency from PyPi as 
`pip install bastion-key-swagger-client`. 

To push Bastion Key Client to PyPi, do
```shell
$ rm dist/*
$ python setup.py sdist bdist_wheel
$ twine upload dist/*
```
from the top level directory

## Principle of operation
The script is designed to be run as a cron job from one or more bastion hosts, periodically interrogating
UIS/CoreAPI `bastionkeys_get` endpoint for new and expired bastion SSH keys. 
It then uses [Ansible](ansible/README.md) to update ~/.ssh/authorized_keys file for each
user whose key has changed, creating user accounts if necessary. 
In addition to avoid stale keys it checks the comments on the keys which have
their expiration date encoded as `..._(2021-11-11 11:11:11+0000)_` and expires/removes those as well.

UIS/CoreAPI provides the keys including the comment-encoded expiration date, login and full name of
each affected user as part of the return of the `bastionkeys_get` endpoint. 

The script saves the last time it ran as UTC timestamp in a file and uses that as a parameter in the next
invocation. If no file exists it uses a preconfigured _backoff_ period to scan for keys. 

The script can reach into any home directory avoiding those that are
specified on a special exclude list as part of its configuration. 
It is assumed accounts listed there do not require automatic key rotation via UIS. 

Formally, the script runs in stages:

1. Execute a call against `bastionkeys_get` and get a list of new and expired keys
2. Collect all new keys and user accounts
3. Scan allowed home directories for expired keys and build a list of keys that need to be expired by appending to 
the list of expired keys received from UIS/CoreAPI
4. Create a single configuration file for the Ansible role with accounts and keys
to be added and removed
5. Execute the ansible playbook to affect the changes

## Design, packaging, permissions and deployment considerations

While it is possible to design the script to run fully remotely, it is more efficient
to have it run locally, since it needs to scan the contents of multiple ~/.authorized_keys
files on the bastion host itself (in Stage 3).

Since the script must modify the state of the bastion host's /etc/passwd, /etc/group and 
/home/.../.ssh/authorized_keys, it runs native to the bastion host (not in a container).
The script does not run on the root account. The script runs with sufficient privilege to
see inside /home/.../.ssh/authorized_keys of all accounts and is able to sudo via 
[Ansible](ansible/README.md) playbooks. 

It is assumed that Python3, Ansible (built-in and posix packages) are installed and available
to the user executing the script.

# Configuration

The behavior of the script is configured largely via a `.env` file (formatted as a set of Bash
variable assignments). The filename is assumed to be `.env` unless `-c` option is used. The
following parameters can be specified:

| Parameter name | (M)andatory or (O)ptional| Default value | Notes |
|--- |--- |--- | --- | 
| UIS_HOST_URL | O | https://127.0.0.1:8443/ |
| UIS_HOST_SSL_VALIDATE | O | True | Warnings from urllib will be printed if `False` |
| UIS_API_SECRET | M |  | 
| TIMESTAMP_FILE | O | /tmp/bastion-timestamp |
| LOCK_FILE | O | /tmp/bastion-timestamp.lock |
| BACKOFF_PERIOD | O | 1440 | In minutes | 
| EXCLUDE_LIST_FILE | O | | Exclude home directories of these users (white space separated)  |
| HOME_PREFIX | O | /home |
| WITH_PREJUDICE | O | False | If `True` remove keys that don't have a timestamp |

# Testing

## Local testing for development

Easiest to spin up a Vagrant VM with CentOS 8 or whatever appropriate, make sure Python3
and Ansible 2.11+ are installed on it. The rough flow of installation commands is as
follows (it is automated in the vagrant setup under `vagrant/`):
```shell
$ sudo dnf update
-- snip -- restart ---
# install python3
$ sudo dnf install python3
# PIP needs to be updated
$ curl https://bootstrap.pypa.io/get-pip.py > get-pip.py
$ python3 get-pip.py
# Install ansible 
$ python3 -m pip install --user ansible
# test 
$ ansible localhost -m ping --ask-pass
$ ansible localhost -m ansible.builtin.setup
```
ansible.cfg 
```ini
[defaults]
deprecation_warnings=False
```
Test playbook
```yaml
- name: update apache locally
  hosts: localhost
  connection: local
  become: yes
  tasks:
  - name: update apache
    ansible.builtin.yum:
      name: httpd
      state: latest
```