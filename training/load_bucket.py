from google.cloud.storage import Client, transfer_manager


def download_bucket_with_transfer_manager(
    bucket_name,
    destination_directory="./data/",
    workers=8,
    max_results=1000,
    project_id="algorithmic-quartet",
):
    storage_client = Client(project=project_id)
    bucket = storage_client.bucket(bucket_name)

    blob_names = [blob.name for blob in bucket.list_blobs(max_results=max_results)]

    results = transfer_manager.download_many_to_path(
        bucket,
        blob_names,
        destination_directory=destination_directory,
        max_workers=workers,
    )

    for name, result in zip(blob_names, results):
        if isinstance(result, Exception):
            print("Failed to download {} due to exception: {}".format(name, result))
        else:
            print("Downloaded {} to {}.".format(name, destination_directory + name))


if __name__ == "__main__":
    # Replace 'your-project-id' with your actual Google Cloud project ID
    download_bucket_with_transfer_manager("zhaw_algorithmic_quartet_training_images")
