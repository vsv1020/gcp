from pprint import pprint
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

credentials = GoogleCredentials.get_application_default()

service = discovery.build('compute', 'v1', credentials=credentials)

# Project ID for this request.
project = 'qijifei-test'  # TODO: Update placeholder value.

# The name of the zone for this request.
zone = 'us-west1-b'  # TODO: Update placeholder value.

body = {  
"sourceInstanceTemplate": "projects/qijifei-test/global/instanceTemplates/instance-template-1" , 
"instanceProperties": {
"KeyName": "test",  
"machineType": "e2-small",
"canIpForward": "False",  
"deletionProtection": "False",  

"networkInterfaces": [  
{ 
"accessConfigs": [  
{ 
"type": "ONE_TO_ONE_NAT", 
"name": "External IP" 
} 
],  
"network": "https://www.googleapis.com/compute/v1/projects/qijifei-test/global/networks/default"  
} 
],  
"tags": { 
"items": [  
"http-server",  
"https-server"  
] 
},
"disks": [
{
      "autoDelete": "true",
      "boot": "true",
      "deviceName": "instance-template-1",
      "initializeParams": {
        "diskSizeGb": "20",
        "diskType": "pd-balanced",
        "labels": {},
        "sourceImage": "projects/centos-cloud/global/images/centos-7-v20210817"
      },
      "mode": "READ_WRITE",
      "type": "PERSISTENT"
    },
{
     "autoDelete": "false",
      "deviceName": "disk-7",
      "diskEncryptionKey": {},
      "initializeParams": {
        "description": "",
        "diskSizeGb": "100",
        "diskType": "pd-ssd"
      },
      "mode": "READ_WRITE",
      "type": "PERSISTENT"
    }

],
"metadata": { 
"items": [
      {
        "key": "startup-script",
        "value": "#!/bin/bash\\n\\necho date > /tmp/startup.log"
      },
      { 
"key": "ssh-keys",  
"value": "root:ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCuRs4aLlU7AQYQOtOpi0WvufqW2CrLIm0bBzc438KYgoOt3OGA4EJsImX4BoOYiOtiG0guLXTC2GBm9KzuObc+94imEKQQOnk4xUQHTT60Eqa2gHIe6BXlOG9HR2s0noxkEcoWrEcwp9bY2E9as6SCBUNvXqaXE7jHUHOg0s6cB5l7c5y+chc5Ja8ypBsMIT9SI/NjW/v7Vdjp17wn4YdHUIKfppZc9uNbO8uonbYVWMw5TjAf8SxYVqrmZ5hw6ubLmKRUlFN/voB4+WCD4brLSHPCuo4TO6RXKcL+foY+nQgbRIoZOomLjSufkAGvkjXKNqb0q51u5mzlYlBGhM+l"  
}, 
      {
        "key": "block-project-ssh-keys",
        "value": "true"
      }
    ]
}
}, 
"labels": { 
"project": "koa", 
"release": "gcp", 
"environment": "stage",
"service": "app", 
"guid": "587e00b0-bf89-11ec-8501-3e22fb84511b"  
},  
"namePattern": "mingli-####",
"count": "2", 
"minCount": "2",
}


request = service.instances().bulkInsert(project=project, zone=zone, body=body)
response = request.execute()

# TODO: Change code below to process the response dict:
pprint(response)

