import boto3
import click
from botocore.exceptions import ClientError

session = boto3.Session(profile_name ='Waqar')
s3 = session.resource('s3')

@click.group()
def cli():
    "S3 all options:"
    pass

@cli.command('List_Buckets')
def List_Buckets():
    "List all buckets in profile"
    for bucket in s3.buckets.all():
        print(bucket)

@cli.command('List_objects')
@click.argument('bucket')
def List_objects(bucket):
    "List objects"
    for obj in s3.Bucket(bucket).objects.all():
        print(obj)

@cli.command('Setup_bucket_static Website')
@click.argument('bucket')
def Setup_bucket_static(bucket):
    "Setup bucket(Create and configure S3)"
    s3_bucket = None
    try:    
        s3_bucket = s3.create_bucket(
            Bucket=bucket,
            CreateBucketConfiguration={
                'LocationConstraint': session.region_name
            }
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
            s3_bucket = s3.Bucket(bucket)
        else:
            raise e

    policy = """
            {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "PublicReadGetObject",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": [
                        "s3:GetObject"
                    ],
                    "Resource": [
                        "arn:aws:s3:::%s/*"
                    ]
                }
            ]
        }
        """ % s3_bucket.name
    policy = policy.strip()
    pol = s3_bucket.policy()
    pol.put(Policy=policy)

    ws = s3_bucket.Website()
    ws.put(WebsiteConfiguration={
        'ErrorDocument': {
            'key': 'error.html'
        },
        'IndexDocument': {
            'Suffix': 'index.html'
        }
    })

if __name__ == '__main__':
    cli()

