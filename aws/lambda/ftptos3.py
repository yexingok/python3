#!/usr/bin/env python

import os
import boto3
from datetime import datetime
from ftplib import FTP


def get_matching_s3_objects(bucket, prefix='', suffix=''):
    """
    Generate objects in an S3 bucket.

    :param bucket: Name of the S3 bucket.
    :param prefix: Only fetch objects whose key starts with
        this prefix (optional).
    :param suffix: Only fetch objects whose keys end with
        this suffix (optional).
    """
    s3 = boto3.client('s3')
    kwargs = {'Bucket': bucket}

    # If the prefix is a single string (not a tuple of strings), we can
    # do the filtering directly in the S3 API.
    if isinstance(prefix, str):
        kwargs['Prefix'] = prefix

    while True:

        # The S3 API response is a large blob of metadata.
        # 'Contents' contains information about the listed objects.
        resp = s3.list_objects_v2(**kwargs)

        try:
            contents = resp['Contents']
        except KeyError:
            return

        for obj in contents:
            key = obj['Key']
            if key.startswith(prefix) and key.endswith(suffix):
                yield obj

        # The S3 API is paginated, returning up to 1000 keys at a time.
        # Pass the continuation token into the next response, until we
        # reach the final page (when this field is missing).
        try:
            kwargs['ContinuationToken'] = resp['NextContinuationToken']
        except KeyError:
            break


def get_matching_s3_keys(bucket, prefix='', suffix=''):
    """
    Generate the keys in an S3 bucket.

    :param bucket: Name of the S3 bucket.
    :param prefix: Only fetch keys that start with this prefix (optional).
    :param suffix: Only fetch keys that end with this suffix (optional).
    """
    for obj in get_matching_s3_objects(bucket, prefix, suffix):
        yield obj['Key']


def ftptos3(ftphost, ftppath, ftpsuffix, bucket, s3path):
    """
    Compare files from S3 and remote FTP, download missing file.

    :param host: Remote ftp host to connect.
    :param ftppath: Remote ftp path where we list to find all files to
                    download
    :param ftpsuffix: Filter we apply to FTP list.
    :param bucket: s3 bucket name to upload file.
    :param s3path: s3 bucket path to upload file.

    """

    # Initalize temp localPath:
    localPath = '/tmp/' + s3path
    os.makedirs(localPath, exist_ok=True)
    s3Files = []
    s3 = boto3.client('s3')

    # Get exists s3 keys
    for key in get_matching_s3_keys(bucket=bucket,
                                    prefix=s3path):
        key = key[key.rfind('/'):].replace('/', '')
        s3Files.append(key)

    with FTP(host=ftphost) as ftp:
        ftp.login()
        ftp.cwd(ftppath)
        ftpFiles = ftp.nlst(ftpsuffix)
        fileToDownload = set(ftpFiles) - set(s3Files)
        fileToDownload = list(fileToDownload)
        print("%d files to download" % len(fileToDownload))
        fileToDownload.sort()
        for filename in fileToDownload:
            localFile = localPath + filename
            try:
                print('Downloading %s' % filename, end=" ")
                with open(localFile, 'wb') as f:
                    ftp.retrbinary('RETR %s' % filename, f.write)
                    print('Finish!')
                ftp.voidcmd('NOOP')
            except Exception as err:
                print('Error: %', err)
                exit(1)
            try:
                print('Uploading %s to s3' % filename, end=" ")
                with open(localFile, 'rb') as f:
                    s3.upload_fileobj(f, bucket, s3path + filename)
                    print('Finish!')
            except Exception as err:
                print('Error: %', err)
            os.remove(localFile)


def main(event, context):
    ftphost = 'ftp.ncbi.nlm.nih.gov'
    ftppath = 'pubmed/updatefiles'
    ftpsuffix = '*.gz'
    bucket = 'mys3bucket'
    s3path = 'pubmed/' + datetime.now().strftime('%Y') + '/updatefiles/'
    ftptos3(ftphost, ftppath, ftpsuffix, bucket, s3path)


if __name__ == "__main__":
    main()
