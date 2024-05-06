from configurations.Configuration import Configuration
from configurations.DevConfig import DevConfig
from datasets import load_dataset
from google.cloud.storage import Client, transfer_manager


def prepare_data(config: Configuration):
    num_of_files = len(list(config.local_dataset_path.glob("*")))

    if not config.local_dataset_path.exists() or num_of_files < config.num_images:
        download_bucket_with_transfer_manager(
            config.training_bucket_name, max_results=config.num_images
        )

    if isinstance(config, DevConfig):
        print("Testing Training pipeline. This will not train the model!")
        print("In order to train the model, pass the -t or --training flag!")

        return load_dataset(
            str(config.local_dataset_path.resolve()),
            split=f"train[0:{config.num_images}]",
        )

    return load_dataset(
        str(config.local_dataset_path.resolve()), split=f"train[0:{config.num_images}]"
    )


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

    print(f"Downloaded {len(blob_names)} files.")


if __name__ == "__main__":
    # Replace 'your-project-id' with your actual Google Cloud project ID
    download_bucket_with_transfer_manager("zhaw_algorithmic_quartet_training_images")
