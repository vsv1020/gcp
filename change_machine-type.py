#!/bin/python3.6
import os

'''
To use Change instance machine-type
'''

def instance_stop(instance_id,zone_name):
    os.system("gcloud compute instances stop %s --zone %s" % (instance_id, zone_name))

def instance_change(instance_id,zone_name,machine_type):
    os.system("gcloud compute instances set-machine-type %s --zone %s --machine-type %s" %(instance_id,zone_name,machine_type))

def instance_start(instance_id,zone_name):
    os.system("gcloud compute instances start %s --zone %s" % (instance_id, zone_name))

def main():
        f = open("instance.list","r")
        for line in f:
            instance_name = line.split(",")[0]
            instance_zone = line.split(",")[1]
            machine_type = line.split(",")[2]
            instance_stop(instance_name,instance_zone)
            instance_change(instance_name,instance_zone,machine_type)
            instance_start(instance_name,instance_zone)
           
            
      
#    os.system('gcloud compute instances list --filter=\"name=(\'zhangtao-test1\')\"')

if __name__ == "__main__":
    main()
