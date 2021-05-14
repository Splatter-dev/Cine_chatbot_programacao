from google.cloud import storage


storage_client = storage.Client()
bucket_name = "html_scraping"
bucket = storage_client.bucket(bucket_name)


def upload_blob(source_file_name, destination_blob_name):

    blob = bucket.blob(f'prog_days/{destination_blob_name}')

    try:
        blob.upload_from_string(source_file_name)
    except:
        print("Erro")


def download_blob(source_file_name):

    blob = bucket.blob(f'prog_days/{source_file_name}')

    try:
        blob_str = blob.download_as_text()
        return blob_str
    except:
        print("Erro")