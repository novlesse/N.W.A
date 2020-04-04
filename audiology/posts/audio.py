import boto3

def upload_file(file_name, bucket):
    """
    Function to upload a file to an S3 bucket
    """

    object_name = "".join(file_name.split())
    s3_client = boto3.client('s3')
    response = s3_client.upload_file(file_name, bucket, object_name)
    return response

def download_file(file_name, bucket):
    """
    Function to download a given file from an S3 bucket
    """
    s3 = boto3.resource('s3')
    output = f"downloads/{file_name}"
    s3.Bucket(bucket).download_file(file_name, output)

    return output

def list_files(bucket):
    """
    Function to list files in a given S3 bucket
    """
    s3 = boto3.client('s3')
    contents = []
    for item in s3.list_objects(Bucket=bucket)['Contents']:
        contents.append(item)

    return contents   
  
def get_bucket_location(file_name, bucket):

    s3 = boto3.resource('s3') 
    # location = s3.get_bucket_location(Bucket=bucket)['LocationConstraint']
    url = 'https://%s.s3-us-west-1.amazonaws.com/uploads/%s' % (bucket, file_name)

    return url 