![PyPI](https://img.shields.io/pypi/v/bastion-key-client?style=plastic)


# BastionKeyClient
Client for automatically managing SSH keys in bastion hosts

## Release notes

### 1.9.0
- Removed vulnerable Authlib dependency (CVE-2026-27962).
- Slimmed `requirements.txt` to direct dependencies with refreshed minimum versions.
- Bumped `python_requires` to `>=3.10`.

## Requirements.

Python 3.10+, Ansible 9.0+ (installed automatically as a dependency)

## Principle of operation
The script is designed to be run as a cron job/systemd timer from every bastion host
UIS/CoreAPI (*UIS* name is used throughout the document, however the new permanent name
of the service is CoreAPI). CoreAPI maintains nearly drop-in compatibility with UIS, which
has been deprecated.

The scripts periodically interrogates `bastionkeys` endpoint for new and expired bastion SSH keys. 
It then uses [Ansible](bastion_key_client/ansible/README.md) to update ~/.ssh/authorized_keys file for each
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

In addition the script uses a `prejudice` setting to decide how to deal with keys found in ~/.ssh/authorized_keys
that do not have expiration timestamps in the comments. If True, those keys are removed when they are found,
if False they are left alone. 

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
to have it run locally, since it needs to scan the contents of multiple 
/home/.../.ssh/authorized_keys files on the bastion host itself (in Stage 3).

Since the script must modify the state of the bastion host's /etc/passwd, /etc/group and 
/home/.../.ssh/authorized_keys, it runs native to the bastion host (not in a container).
The script does not run on the root account. The script runs with sufficient privilege to
see/modify inside /home/.../.ssh/authorized_keys of all accounts and is able to sudo via 
[Ansible](bastion_key_client/ansible/README.md) playbooks to modify create new accounts. 

It is assumed that Python3, Ansible (built-in and posix packages) are installed and available
to the user executing the script (Ansible is installed as a dependency).

## Directory Structure and Dev Installation

Note: the client no longer relies on auto-generated Swagger client stubs and invokes the CoreAPI directly.

To push Bastion Key Client to PyPi, do
```shell
$ rm dist/*
$ python -m build
$ twine upload dist/*
```
from the top level directory

## Production installation and invocation

Since the script must be executed as sudo, it is recommended that the script package is
installed via sudo (Ansible is installed automatically as a dependency):
```bash
$ sudo pip3 install bastion-key-client
```

If deploying as non root, it is recommended that `/usr/local/bin` is added to `secure_path` in `/etc/sudoers/` 
or else the script is symlinked to `/usr/bin` (a more secure approach). The script can then be invoked 
(using absolute paths, after creating appropriate configuration files):
```
$ sudo /usr/local/bin/update_bastion_keys.py -c /home/vagrant/bastion-env
```
For crontab deployment, remember that cron jobs have no access to environment variables, including PATH
so be sure to add /usr/local/bin to PATH for crontab configuration:
```
PATH=/bin:/sbin/:/usr/bin:/usr/sbin:/usr/local/bin
* * * * * /usr/local/bin/update_bastion_keys.py -c /root/.update_bastion_keys.env
```
or alternatively
```
* * * * * export PATH=/usr/bin:/usr/local/bin; /usr/local/bin/update_bastion_keys.py -c /root/.update_bastion_keys.env
```

Note that SSHd must be configured to disallow SCP and SFTP for all users whose keys are managed by this script 
otherwise they can manipulate allowed keys outside of the control of UIS. Additionally TTY creation must be
disallowed  (selectively for accounts managed by this script or globally for the host) in order to prevent 
users from logging into the bastion host and directly manipulating the keys. The following options can be used 
in `sshd_config`: 

```
X11Forwarding no
PermitTTY no
```
## Configuration

The behavior of the script is configured largely via a `.env` file (formatted as a set of Bash
variable assignments). The filename is assumed to be `.env` unless `-c` option is used. The
following parameters can be specified:

| Parameter name        | (M)andatory or (O)ptional | Default value               | Notes                                                                                                                                                         |
|-----------------------|---------------------------|-----------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|
| UIS_HOST_URL          | O                         | https://127.0.0.1:8443/     | UIS/CoreAPI URL                                                                                                                                               |
| UIS_HOST_SSL_VALIDATE | O                         | True                        | UIS/CoreAPI SSL validation. Warnings from urllib will be printed if `False`                                                                                   |
| UIS_API_SECRET        | M                         |                             | UIS/CoreAPI secret string                                                                                                                                     |
| TIMESTAMP_FILE        | O                         | /tmp/bastion-timestamp      |                                                                                                                                                               |
| LOCK_FILE             | O                         | /tmp/bastion-timestamp.lock |                                                                                                                                                               |
| LOG_FILE              | O                         | stdout                      | Can be 'stdout' or a file name                                                                                                                                | 
| EXTRA_VARS_FILE       | O                         | /tmp/bastion-users.json     | File to which --extra-vars (account and key information) of the Ansible role are saved prior to execution. Normally deleted after completion.                 |
| BACKOFF_PERIOD        | O                         | 1440                        | In minutes                                                                                                                                                    | 
| EXCLUDE_LIST_FILE     | M                         |                             | Exclude home directories of these users (white space separated). To serve as a reminder, no default is provided, script exits with an error if not specified. |
| HOME_PREFIX           | O                         | /home                       |
| WITH_PREJUDICE        | O                         | False                       | If `True` remove keys that don't have a timestamp                                                                                                             |

## Logging

Logging from the script can be set to go to `stdout` (default configuration) or set LOG_FILE configuration
variable to an absolute path of the log file (see Configuration section). 

If using `-d` debug option, `stdout` is always used for logging and LOG_FILE setting is ignored.

In addition the built-in ansible role has an ansible.cfg file that sets log path to `/tmp/bastion-ansible.log`.
You can change this configuration on an already deployed system by editing this file typically located
some place like `/usr/local/lib/python3.10/site-packages/bastion_key_client/ansible/fabric-bastion/ansible.cfg`.

## Testing

### Smoke test with Docker

A quick way to verify the package installs and imports correctly:
```bash
$ docker run --rm -v $(pwd):/app -w /app python:3.10-slim \
    sh -c "pip install . && python -c 'import bastion_key_client; print(bastion_key_client.__VERSION__)'"
```

### Test mode

The script supports a `-t` flag that queries the CoreAPI endpoint and generates the Ansible
extra-vars JSON file without executing the playbook. Combined with `-d` for debug output:
```bash
$ update_bastion_keys.py -c /path/to/.env -t -d
```
This validates API connectivity, authentication, and key parsing without modifying the host.

### Local testing for development

Spin up a VM (e.g., AlmaLinux 9 or similar) with Python 3.10+ installed.
The [Vagrantfile](vagrant/centos8/Vagrantfile) provides a starting point but
references CentOS 8 (EOL) and may need updating for current OS images.

Create a `.env` configuration file and execute manually or via cron/systemd timer.