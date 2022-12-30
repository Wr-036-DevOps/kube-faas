from bing_image_downloader import downloader
import json
import boto3
import os


def handle(event):
    print(event)
    event_dict = json.loads(event)
    # Extracting parameter from the SQS json mesage #Python dictionary
    # data = event_dict["Records"][0]["body"]
    animal = event_dict["animal"]
    number = int(event_dict['number'])
    


    # Downloading the number of pictures of given animal
    print(f"we are downloading {number} pictures of {animal}")
    downloader.download(f"{animal}", limit=number, output_dir='dataset', adult_filter_off=True, force_replace=False, timeout=60)

    bucket_name = "wr-36-animal-images"
    path = f"./dataset/{animal}/"
    client = boto3.client("s3")


    # Uploading downloaded images to s3
    for i, image in enumerate(os.listdir(path)):
        # Create the new filename using the animal name and the loop index
        new_filename = f"{animal}-{i + 1}.jpg"

        # Use the os.rename() function to rename the file
        os.rename(os.path.join(path, image), os.path.join(path, new_filename))
        key = new_filename

        # Creating file name with full path for open()
        file = str(path) + str(new_filename)
        with open(file, "rb") as f:
            client.put_object(
                Bucket=bucket_name,
                Body=f,
                Key=key
            )

    return {
        'statusCode': 200,
        'body': f"upload succeeded: upload of {number} images of {animal} complete"
    }