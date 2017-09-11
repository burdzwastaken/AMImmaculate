import boto3
import os
import re
from datetime import datetime, timedelta
from itertools import chain

client = boto3.client('ec2')
ec2 = boto3.resource('ec2', 'us-east-1')
ec2Regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
ownerID = boto3.client('sts').get_caller_identity().get('Account')
allowedAge = datetime.now()-timedelta(days=int(os.environ['allowedAge'])) 

def lambda_handler(event, context):

    for region in ec2Regions:
        conn = boto3.resource('ec2', region_name=region)
        myImages = conn.images.filter(Owners=[ownerID])

        usedImages = set([instance.image_id for instance in conn.instances.all()])
        print "Used images to exclude from deregistering in %s:" % region
        print usedImages

        exclusionTags = [{'Name':'tag:Name', 'Values':['important-amis-*']}]
        taggedImages = set([image.id for image in conn.images.filter(Filters=exclusionTags)])
        print "Tagged images to exclude from deregistering in %s:" % region
        print taggedImages

        deregisterList = {image.id: image for image in myImages if image.id not in chain(usedImages, taggedImages)}
        print "AMIs to be degegistered:"
        print deregisterList
        print "Deregistering AMIs in %s:" % region

        for image in deregisterList.values():
            createdDate = datetime.strptime(
                image.creation_date, "%Y-%m-%dT%H:%M:%S.000Z")
            if createdDate < allowedAge:
                image.deregister()

        print "Deleting snapshots in %s:" % region
        myImages = conn.images.filter(Owners=[ownerID])
        images = [image.id for image in myImages]  
        for snapshot in conn.snapshots.filter(OwnerIds=[ownerID]):  
            r = re.match(r".*for (ami-.*) from.*", snapshot.description)
            if r:
                if r.groups()[0] not in images:
                    print "Snapshot to be deleted:"
                    print snapshot
                    snapshot.delete()

