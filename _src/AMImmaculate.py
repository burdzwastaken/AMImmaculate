import boto3
import os
from datetime import datetime, timedelta

client = boto3.client('ec2')
ec2 = boto3.resource('ec2', "us-east-1")
ec2_regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
owner_id = boto3.client('sts').get_caller_identity().get('Account')
allowed_age = datetime.now()-timedelta(days=os.environ['allowed_age']) 

def lambda_handler(event, context):

    for region in ec2_regions:
        conn = boto3.resource('ec2', region_name=region)
        my_images = conn.images.filter(Owners=[owner_id])
        good_images = set([instance.image_id for instance in conn.instances.all()])  
        print "Images to exclude from deregistering in %s:" % region
        print good_images

        my_images_dict = {image.id: image for image in my_images if image.id not in good_images}  
        print "About to deregister the following AMIs in %s:" % region
        print my_images_dict

        for image in image.values():  
            created_date = datetime.strptime(
                image.creation_date, "%Y-%m-%dT%H:%M:%S.000Z")
            if created_date < allowed_age:
                image.deregister()
