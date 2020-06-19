
from __future__ import print_function
from argparse import ArgumentParser
import boto3
from botocore.exceptions import ClientError


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        print(e)
        return False
    return True


def create_presigned_url(bucket_name, object_name, expiration=3600):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        print(e)
        return None

    # The response contains the presigned URL
    return response

def main(f, bucket, job_id):
    upload_file(f, bucket, job_id)
    return create_presigned_url(bucket, job_id, 86400)

if __name__ == '__main__':
    userInput = ArgumentParser()
    requiredNamed = userInput.add_argument_group('required arguments')
    requiredNamed.add_argument('-f', '--File', action='store', required=True,
                                help='file path.')
    requiredNamed.add_argument('-b', '--Bucket', action='store', required=True,
                                help='bucket name.')
    requiredNamed.add_argument('-j', '--Job', action='store', required=True,
                                help='job id.')
    args = userInput.parse_args()
    f = args.File
    bucket = args.Bucket
    job_id = args.Job

    main(f, bucket, job_id)
    