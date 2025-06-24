import boto3
import datetime


def lambda_handler(event, context):
    bucket_name = 'jay-s3-cleanup-bucket-9912'  # Replace with your actual new bucket name
    days_threshold = 30


    s3 = boto3.client('s3')
    now = datetime.datetime.now(datetime.timezone.utc)


    response = s3.list_objects_v2(Bucket=bucket_name)


    if 'Contents' not in response:
        print("Bucket is empty.")
        return


    for obj in response['Contents']:
        key = obj['Key']
        last_modified = obj['LastModified']


        # Simulate older file if name contains "old"
        if 'old' in key.lower():
            simulated_time = now - datetime.timedelta(days=31)
            age = (now - simulated_time).days
        else:
            age = (now - last_modified).days


        if age > days_threshold:
            print(f"Deleting: {key} (Age: {age} days)")
            s3.delete_object(Bucket=bucket_name, Key=key)
        else:
            print(f"Keeping: {key} (Age: {age} days)")
