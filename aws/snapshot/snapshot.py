#!/usr/bin/env python

import boto3
from datetime import datetime, timedelta
from pytz import timezone


def backup_snapshot(tag='backup', dryrun=False):
    ''' Create snapshot for instance have backup = true tag , backup all volumes attached with this instance, if a volume have backup = false tag, will skip this volume.
    '''
    ec2 = boto3.resource('ec2')
    filter = [{
        'Name': 'tag:backup',
        'Values': ['true', 'True']
    }]
    for instance in ec2.instances.all().filter(Filters=filter):
        volumes_to_process = []
        for volume in instance.volumes.all():
            if volume.tags == None:
                volumes_to_process.append(volume)
            else:
                volume_tags_dict = {x['Key']: x['Value'] for x in volume.tags}
                if 'backup' in volume_tags_dict:
                    if volume_tags_dict['backup'] == 'false' or volume_tags_dict['backup'] == 'False':
                        pass
                    else:
                        volumes_to_process.append(volume)
                else:
                    volumes_to_process.append(volume)
        volume_ids = [x.id for x in volumes_to_process]
        print 'Process instance {0} volume {1}'.format(instance.id, volume_ids)
        instance_tags_dict = {x['Key']: x['Value'] for x in instance.tags}
        for volume in volumes_to_process:
            device_name = volume.attachments[0]['Device']
            snapshot_description = instance_tags_dict['Name'] + \
                ' | ' + device_name
            snapshot = volume.create_snapshot(
                Description=snapshot_description, DryRun=dryrun)
            snapshot_tags = [
                {
                    'Key': 'instance',
                    'Value': instance.id
                },
                {
                    'Key': 'device_name',
                    'Value': device_name
                },
                {
                    'Key': 'backupwith',
                    'Value': 'boto3'
                }
            ]
            snapshot.create_tags(Tags=snapshot_tags, DryRun=dryrun)


def del_old_snapshot(keepdate=14, dryrun=False):
    ''' Loop all the snapshots in the region, and try to remove snapshots larger than keepdate, skip first day of month and AMI generated from console, for the first day of month snapshot, keep most for one year.
    '''
    ec2 = boto3.resource('ec2')
    for snapshot in ec2.snapshots.all().filter(OwnerIds=['self']):
        snapshot_time_cst = snapshot.start_time.astimezone(
            timezone('Asia/Shanghai'))
        snapshot_day = datetime.strftime(snapshot_time_cst, "%d")
        # skip some snapshots
        if snapshot.description.find("CreateImage") > -1:
            continue
        now_cst = datetime.now(timezone('Asia/Shanghai'))
        if snapshot_day == '01' and ((now_cst - snapshot_time_cst) < timedelta(days=365)):
            continue
        is_old_snapshot = (
            now_cst - snapshot_time_cst) > timedelta(days=keepdate)
        if is_old_snapshot:
            print "Try to remove snapshot: {}, description: {}, snapshot_time: {}".format(snapshot.id, snapshot.description, snapshot_time_cst)
            try:
                snapshot.delete(DryRun=dryrun)
            except:
                print "Failed to remove snapshot: {}, it may be an AMI.".format(snapshot.id)


def all_regions():
    client = boto3.client('ec2')
    response = client.describe_regions()
    return response['Regions']


for region in all_regions():
    print "Processing Region: {}".format(region['RegionName'])
    boto3.setup_default_session(region_name=region['RegionName'])
    backup_snapshot()
    del_old_snapshot()
