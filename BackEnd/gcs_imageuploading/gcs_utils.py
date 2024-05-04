# gcs_utils.py

from google.cloud import storage

def upload_image_to_gcs(bucket_name, local_file_path, destination_blob_name):
    # Initialize the client
    client = storage.Client()

    # Get the bucket
    bucket = client.bucket(bucket_name)

    # Upload the file
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(local_file_path)

    print(f"File {local_file_path} uploaded to {destination_blob_name}.")
