from bing_image_downloader import downloader
import json


def handle(event):
    event_dict = json.loads(event)
    # Extracting parameter from the SQS json mesage #Python dictionary
    data = event_dict["Records"][0]["body"]
    animal = data["animal"]
    number = int(data['number'])
    


    # Downloading the number of pictures of given animal
    print(f"we are downloading {number} pictures of {animal}")
    downloader.download(f"{animal}", limit=number, output_dir='dataset', adult_filter_off=True, force_replace=False, timeout=60)

    return {
        'statusCode': 200,
        'body': f"download succeeded: download of {number} images of {animal} complete"
    }