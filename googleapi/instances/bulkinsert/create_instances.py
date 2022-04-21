from pprint import pprint

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

credentials = GoogleCredentials.get_application_default()

service = discovery.build('compute', 'v1', credentials=credentials)

# Project ID for this request.
project = 'qijifei-test'  # TODO: Update placeholder value.

# The name of the zone for this request.
zone = 'us-central1-a'  # TODO: Update placeholder value.

body = {
    "count": "2",
    "canIpForward": "False",
    "labels": {
            "project": "koa",
            "release": "gcp",
            "environment": "stage",
            "service": "app",
            "guid": "587e00b0-bf89-11ec-8501-3e22fb84511b"
    },
    "machineType": "zones/us-west1-b/machineTypes/e2-medium",
    "metadata": {
      "items": [
        {
          "key": "ssh-keys",
          "value": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDSH6zOb41hoGE2NcYrYIhLlAsizy1yaE5P25bD9DIQ7iralJNQsR879XSki5YpSSlmIGp4d8sSCS9hWTPpBb+ogOVtmluQ/pLdsycjKJ0qOT487bEQLF9aKIPvZCQ8dwS7d+EURk1x4/PpnCwCZZWaKHKNmdn5OlVDtkra/iZUgs53I4yQ1WBD4CUbEsz87jIP2m8/p5BCfT9YfTqiHA/dT055lQ5HCG6bdW2lfZQFwZEFoLk++a1aB61HLJNjqWzuc3BeG2UYaDd48aLGTHmfjtJUSStOUvO7Z2yxfn7wFLA5dWH37hbTZFmTYfNrZbujftuQK/cA6neNi/OwVuNrq/PfSqutVbs3eTyptDqthIa5nP5MKr5cKEiK/8S/spcBjHXS6y8QQxJtYW143ZZiMEXqb+N0e8HpMAD1VfkMEuaPRTO1iS0pSTPY8DldZb0zvuiWI2FuCgpQ8w0kiSMCNcZrXrVPSdfNI0pe3gvxRhfXOnfgU1AuUJf40OZ2Cy0= root@a01zhangtao-test"
        },
        {
          "key": "startup-script",
          "value": "#!/bin/bash\n\necho `date` > /tmp/startup.log"
        }
      ]
    },
    "networkInterfaces": [
      {
        "accessConfigs": [
          {
            "name": "External IP",
            "type": "ONE_TO_ONE_NAT"
          }
        ],
        "name": "nic0",
        "network": "https://www.googleapis.com/compute/v1/projects/qijifei-test/global/networks/default"
      }
    ],
    "tags": {
      "items": [
        "http-server"
      ]
   },
    "reservationAffinity": {
         "reservationAffinity": {
    			"consumeReservationType": "NO_RESERVATION"
 		 }
        },
     "minCount": "2",
     "namePattern": "zhangtao-####",
     "sourceInstanceTemplate": "projects/qijifei-test/global/instanceTemplates/funplus-template"
}


request = service.instances().bulkInsert(project=project, zone=zone, body=body)
response = request.execute()

# TODO: Change code below to process the response dict:
pprint(response)

