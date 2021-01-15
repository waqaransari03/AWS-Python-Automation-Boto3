import boto3
import click
session = boto3.Session(profile_name='Waqar')

s3 = session.resource('s3')

@click.group()
def cli():
    "my static website to AWS"
    pass
    
@cli.command('list-buckets')
def list_buckets():
    "List all s3 buckets"
    for bucket in s3.buckets.all():
        print(bucket)

@cli.command('get_objects_from_bucket')
@click.argument('bucket')
def get_objects_from_bucket(bucket):
    "get objects from bucket"
    for obj in s3.Bucket(bucket).ojects.all():
        print (obj)

    
if __name__ == '__main__':
    cli()