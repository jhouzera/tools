import boto3
import re
import os

def ebs_cleanup():

    region = os.environ['AWS_REGION']

    # Setting client for search volumes
    ec2 = boto3.client('ec2', region_name=(region))
    ebs_volumes = ec2.describe_volumes(
        Filters=[
        {
            'Name': 'status',
            'Values': [
                'available',
            ]
        },
        ]
    )
    # Getting Volumes
    volumes = ebs_volumes['Volumes']
    # Setting regex variable
    regex_pattern = "kubernetes.*"

    print ("Starting EBS Cleanup!")
    
    for volume in volumes:
        print ("Trying to get volume to create snapshot and delete it...")
        try:
            Tags = volume['Tags']
            VolID = volume['VolumeId']
            for j in range (len(Tags)):
                if (re.search(regex_pattern,(Tags[j]['Key']))) or (re.search(regex_pattern,(Tags[j]['Value']))):
                    print ("{0}: It's not allowed to delete this volume, because is the pvc type!".format(VolID))
                    break
                else:
                    print ("{0}: Will be deleted!".format(VolID))
                    print ("Creating snapshot of Volume {0}...".format(VolID))
                    snapshot = ec2.create_snapshot(VolumeId=VolID,TagSpecifications=[
                        {
                            'ResourceType': 'snapshot',
                            'Tags': Tags
                        }
                    ])
                    SnapshotId = snapshot['SnapshotId']
                    print("Snapshot {0} created for volume {1} with success!".format(SnapshotId,VolID))
                    print ("Deleting volume after create snapshot..".format(VolID))
                    ebs_volumes = ec2.delete_volume(VolumeId=(VolID))
                    print ("Volume {0} was delete with success!".format(VolID))
        except KeyError as e:
            # If there are volume without tags, than creates snapshot and deletes it too
            VolID = volume['VolumeId']
            print ("{0}: This volume is without Tag!".format(VolID))
            print ("Creating snapshot of Volume...")
            snapshot = ec2.create_snapshot(VolumeId=VolID)
            SnapshotId = snapshot['SnapshotId']
            print("Snapshot {0} created for volume {1} with success!".format(SnapshotId,VolID))
            print ("Deleting volume after create snapshot...".format(VolID))
            ebs_volumes = ec2.delete_volume(VolumeId=(VolID))
            print ("Volume {0} was delete with success!".format(VolID))

    print ("EBS Cleanup finished!")

ebs_cleanup()