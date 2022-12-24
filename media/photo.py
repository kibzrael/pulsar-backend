import io
from typing import List
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile

from firebase_admin import storage
from firebase_admin.storage import bucket
from google.cloud.storage import blob

from media.cert import firebase_initialization


def upload_photo(img: InMemoryUploadedFile, path: str, previous_links: List) -> List:
    firebase_initialization()

    default_bucket: bucket = storage.bucket()

    urls: List = []
    blobs: List = []

    resolutions = [
        {"name": "thumbnail", "dimensions": 120},
        {"name": "medium", "dimensions": 240},
        {"name": "high", "dimensions": 480},
    ]

    # index = 0
    for resolution in resolutions:
        pil_image: Image = Image.open(img)
        width = resolution.get("dimensions")
        wpercent = width / float(pil_image.size[0])
        height = int(float(pil_image.size[1]) * float(wpercent))
        resized_image = pil_image.resize((width, height), Image.ANTIALIAS)
        image_bytes = io.BytesIO()
        resized_image.save(image_bytes, "jpeg")
        resized_image.close()
        image_blob: blob = default_bucket.blob(f'{path}-{resolution.get("name")}.jpg')
        blobs.append(f'{path}-{resolution.get("name")}.jpg')
        image_blob.upload_from_string(image_bytes.getvalue(), content_type="image/jpeg")

        image_blob.make_public()

        # signed_url = image_blob.generate_signed_url(datetime(2490,6,30))
        # previous_link =None
        # if len(previous_links)>index:
        #     previous_link = previous_links[index]
        # short_url = shorten_url(signed_url, previous_link)
        # #
        # # Delete previous short url, or use same name
        # #
        # index+=1
        urls.append(image_blob.public_url)

    return [*urls, *blobs]
