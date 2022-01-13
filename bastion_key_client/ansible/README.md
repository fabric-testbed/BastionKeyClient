# User Management Ansible Role
Add/remove user dynamically

- Create a JSON file that includes the variables

Example: 

File: `/var/tmp/user.json`

```
{
   "community": {
      "experimenter": [
         {
            "username": "jdoe",
            "name": "John Doe,,,,jdoe@email.com",
            "shell": "/sbin/nologin",
            "groups": "",
            "state": "present",
            "remove": "yes",
            "force": "yes",
            "create_home": "yes",
            "fabric_role": "regular",
            "ssh_key": [
               {
                  "key": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC0oGeSWTeV0hnROZrkv9w1ZCU/zITZhYiJLE3ylMhQAYK/gFDCXjnxq/p9HaRlTvkLQKtDc0RpvhGfrx6c7Vxbd81ni6WP3pQmt2cQmDpJ6UeDptOCcHk/HkAYT0UM4LzK0gI8pI3a5ziBf2cXCTSrSe52WBsmb//sFFecrs0vUsNP8I8C5aaUKJyO+ujwr5NiN3j3GKJ1AJG1t21qr7dGn8XGAxh1M7BsKwDFuTiS6rPA9rixLg01TK1Pq3qq1MUMo3Cuztpd8xQ8Q/wiVKJQ+029zynLEiL25hBI4c+dhfVlRFnQsb3usE9MH7cv8nigxibuhDO6F6KAvO2utuHG772zv75QEZ/R2NRuyhBMV5pmYFZfOKTPWrrKHnDLXiIT6Etx3rBobzBb/EHH+CCfPto585oXU9EepO320fCTxMGom/5iak1T6scZFcm9wcCP0KIAm/hlKPZWXS7Vs9VcFYE7vrl4rTe8DYzUMoyC4lP/VQNZNqR0HFqBVrUEraE= gburdell@fabric",
                  "state": "present",
               },
               {
                  "key": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDPqNzJFqYTE9GtmhdQYu1SDApVf49lqmEq15FImDBPxYAXsQI5hvBwPJ1SpbMn3f4Z/Q1utxCsLR3J/Z3CO0w1PO4U0gqgL9a0P6F4GW04n/+ObitDasbwFGHHvhWG78IRgHnb2BnTDvnob28V0audsLBQvYfjuVhhwsy4/eM37Xxeoxy2StXXmE/l/g0MIJzwpOy51BiKwp/wjLwogQUufetKIdEOgEGu9kHIMighYQ3CnBRvHTRaqCs/gwLCAnB8nyCEFkaOIsdyEp2iIyHqN9QBKBCxZR/G6jydiIT9zdVRnZ7BmfHeo2jupTJ5Bcuoura04D6F/8LbdnuPRL4CM+wKEwdsDS08qMrk70cIUhDPapvE3ArTMRed05tkQH9IC7/jt5PyjFS0x/N48d4Svdv11GfIq6ftwfZNvGwekDzxTnMTDR3rKeHMScQJGp4ZJv4xl8htZC+a89IAMvYI4VQdN1F49KgW1kOWR4nkUprXkdovExMm1fE13M7I1RE= gburdell@gatech",
                  "state": "absent",
               }
            ]
         }
      ]
   }
}

```

- Adding and removing user accounts is controlled by setting `state` to `present` or `absent`. This includes
manipulating both /etc/passwd and /etc/group
- Adding and removing keys is controlled by setting `state` in `ssh_key` to `present` or `absent`
- `name` can be just full name, however preferred to be formatted as a GECOS field

- Execute ansible task
```
ansible-playbook site.yml --tags "user-experimenter-dynamic" --extra-vars "@/tmp/user.json"
```
