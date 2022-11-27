from datetime import datetime
import subprocess
from tempfile import TemporaryFile
from typing import List
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile

# import ffmpeg
from firebase_admin import storage
from firebase_admin.storage import bucket
from google.cloud.storage import blob
from media.cert import firebase_initialization
from media.cuttly import shorten_url


def upload_video(
    source: InMemoryUploadedFile,
    path: str,
    source_medium: InMemoryUploadedFile,
    source_low: InMemoryUploadedFile,
):
    firebase_initialization()

    default_bucket: bucket = storage.bucket()

    urls: List = []
    blobs: List = []

    resolutions = [
        {
            "name": "low",
            "fps": "21",
            "frame size": "320",
            "audio bitrate": "64K",
            "video bitrate": "320K",
        },
        {
            "name": "medium",
            "fps": "24",
            "frame size": "480",
            "audio bitrate": "96K",
            "video bitrate": "480K",
        },
        {
            "name": "high",
            "fps": "27",
            "frame size": "640",
            "audio bitrate": "128K",
            "video bitrate": "640K",
        },
    ]

    # temp_file = TemporaryFile()
    # loaded_stream = ffmpeg.input('pipe:')
    # output_streams = []

    # for resolution in resolutions:
    #     video = loaded_stream.video.filter('fps', fps=resolution['fps'], round='up').filter(
    #         'scale', resolution["frame size"], -2)
    #     audio = loaded_stream.audio
    #     stream = ffmpeg.output(
    #         video, audio, f'{temp_file.name}-{resolution["name"]}.mp4',
    #         video_bitrate=resolution['video bitrate'],
    #         audio_bitrate=resolution['audio bitrate'])
    #     output_streams.append(stream)

    # ffmpeg.merge_outputs(*output_streams).run(input=source.file.read())

    files: List = []

    if source_medium and source_low:
        files = [source_low, source_medium, source]
    else:

        temp_dir = "/tmp"
        now = datetime.now()
        cmd = ["ffmpeg", "-i", "pipe:"]

        for resolution in resolutions:
            cmd = [
                *cmd,
                "-vf",
                f'scale={resolution["frame size"]}:-2',
                "-r",
                f'{resolution["fps"]}',
                "-b:v",
                f'{resolution["video bitrate"]}',
                "-b:a",
                f'{resolution["audio bitrate"]}',
                f'{temp_dir}/{now}-{resolution["name"]}.mp4',
            ]

        print("starting.....")
        out = subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, input=source.read()
        )
        print("out.....")
        print(out.stdout)
        print("err.....")
        print(out.stderr)

    index = 0

    for resolution in resolutions:
        video_blob: blob = default_bucket.blob(f'{path}-{resolution["name"]}.mp4')
        blobs.append(f'{path}-{resolution["name"]}.mp4')
        # TODO Use source_medium and source_high if ffmpeg fails
        if len(files) < 1:
            video_blob.upload_from_filename(
                f'{temp_dir}/{now}-{resolution["name"]}.mp4', content_type="video/mp4"
            )
        else:
            video_blob.upload_from_string(files[index].read(), content_type="video/mp4")

        video_blob.make_public()
        urls.append(video_blob.public_url)
        index += 1
        # signed_url = video_blob.generate_signed_url(datetime(2490,6,30))
        # short_url = shorten_url(signed_url,None)
        # urls.append(short_url)
        # print(short_url)

    return [*urls, *blobs]
