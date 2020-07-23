#! /usr/bin/python

import hashlib
import json
import sys
import time
import urllib
from pathlib import Path
import os
import shutil

import boto3

from botocore.client import ClientError

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from settings import (
    AWS_ACCESS_KEY_ID,
    AWS_BUCKET_NAME,
    AWS_REGION_NAME,
    AWS_SECRET_ACCESS_KEY,
    logging,
)


TRIM_START = 0  # seconds
TRIM_END = 59  # seconds


def process(input_path, output_dir=None, trim=True):

    input_path = Path(input_path).resolve()
    output_dir = Path(output_dir).resolve() if output_dir else input_path.parent

    # create output dir
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    output_file = input_path.stem + "_sample" + input_path.suffix
    output_path = output_dir / output_file
    json_file = input_path.stem + "_sample.json"
    json_path = output_dir / json_file
    txt_file = input_path.stem + "_sample.txt"
    txt_path = output_dir / txt_file

    # convert to strings
    input_path = str(input_path)
    output_path = str(output_path)
    json_path = str(json_path)
    txt_path = str(txt_path)

    ##############
    # TRIM VIDEO #
    ##############

    if trim:
        logging.info("Trimming video: %s" % input_path)

        # trim video
        ffmpeg_extract_subclip(input_path, TRIM_START, TRIM_END, targetname=output_path)
        logging.info("Saved to: %s" % output_path)
    else:
        logging.info("Coppied video: %s" % output_path)

        # copy video
        shutil.copy(input_path, output_path)

    ####################
    # UPLOAD TO AWS S3 #
    ####################

    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION_NAME,
    )
    logging.info("Uploading to S3")

    # create bucket
    try:
        s3.create_bucket(
            Bucket=AWS_BUCKET_NAME,
            CreateBucketConfiguration={"LocationConstraint": AWS_REGION_NAME},
        )
    except ClientError as e:
        logging.warning(e)

    # upload file
    s3.upload_file(output_path, AWS_BUCKET_NAME, output_path)
    logging.info("Uploaded file: %s" % output_path)

    ######################
    # TRANSCRIBE S3 FILE #
    ######################

    output_hash = hashlib.md5(open(output_path, "rb").read()).hexdigest()
    logging.info("File hash: %s" % output_hash)

    transcribe = boto3.client(
        "transcribe",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION_NAME,
    )

    try:
        transcribe.start_transcription_job(
            TranscriptionJobName=output_hash,
            Media={"MediaFileUri": "s3://%s/%s" % (AWS_BUCKET_NAME, output_path)},
            MediaFormat="mp4",
            LanguageCode="en-IN",
        )
    except ClientError as e:
        logging.warning(e)

    while True:
        response = transcribe.get_transcription_job(TranscriptionJobName=output_hash)

        if response["TranscriptionJob"]["TranscriptionJobStatus"] in [
            "COMPLETED",
            "FAILED",
        ]:
            # save transcribe json
            uri = response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
            urllib.request.urlretrieve(uri, json_path)

            logging.info("Transcribing (COMPLETE): %s" % json_path)
            break

        logging.info("Processing ...")
        time.sleep(5)

    # create transcribe txt
    transcript = ""

    for t in json.load(open(json_path))["results"]["transcripts"]:
        transcript += t["transcript"]

    open(txt_path, "w+").write(transcript)

    logging.info("Transcript (READY): %s" % txt_path)

    return {
        "sample": output_path,
        "json": json_path,
        "txt": txt_path,
    }


if __name__ == "__main__":
    INPUT_PATH = sys.argv[1]
    OUTPUT_DIR = sys.argv[2] if len(sys.argv) >= 3 else None

    paths = process(input_path=INPUT_PATH, output_dir=OUTPUT_DIR, trim=False)

    logging.info("Result: %s" % paths)
