import os
import boto3
from botocore.exceptions import NoCredentialsError


# Function to upload to s3
def upload_to_aws(bucket, local_file, s3_file, aws_access_key, aws_secret):
    """local_file, s3_file can be paths"""
    s3 = boto3.client('s3',
                      aws_access_key_id=aws_access_key,
                      aws_secret_access_key=aws_secret
    )
    
    print('  Uploading ' + local_file + ' as ' + bucket + '/' +s3_file)
    
    try:
        s3.upload_file(
            local_file,
            bucket,
            s3_file,
            ExtraArgs={'ACL': 'public-read'}
            )
        print('  ' + s3_file + ": Upload Successful")
        print('---------')
        return True
    except NoCredentialsError:
        print("Credentials not available")
        return False


def _start(local_folder: str, s3_folder: str, bucket_name:str, host:str):
    
    walks = os.walk(local_folder)

    """For file names"""
    for source, dirs, files in walks:
        print('Directory: ' + source)
        for filename in files:
            # construct the full local path
            local_file = os.path.join(source, filename)
            # construct the full Dropbox path
            relative_path = os.path.relpath(local_file, local_folder)
            s3_file = os.path.join(s3_folder, relative_path)
            # Invoke upload function
            upload_to_aws(bucket_name, local_file, s3_file)

if __name__ == '__main__':
    _start("./tmp/banners/", "banners/", "XXXXXXXX-develop", "https://s3.amazonaws.com/XXXXXXXX/")
