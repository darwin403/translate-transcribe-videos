#! /usr/bin/python

import hashlib
import json
import sys
import time
import urllib
from pathlib import Path

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


def process(INPUT_PATH, OUTPUT_DIR=None):

    input_path = Path(INPUT_PATH).resolve()
    output_dir = Path(OUTPUT_DIR).resolve() if OUTPUT_DIR else input_path.parent
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
    logging.info("Trimming video: %s" % input_path)

    # trim video
    ffmpeg_extract_subclip(input_path, TRIM_START, TRIM_END, targetname=output_path)
    logging.info("Saved to: %s" % output_path)

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
    try:
        s3.head_object(Bucket=AWS_BUCKET_NAME, Key=output_path)
        logging.info("Uploaded file (EXISTS): %s" % output_path)
    except ClientError as e:
        s3.upload_file(output_path, AWS_BUCKET_NAME, output_path)
        logging.info("Uploaded file: %s" % output_path)

    ######################
    # TRANSCRIBE S3 FILE #
    ######################

    output_hash = hashlib.md5(open(output_path, "rb").read()).hexdigest()

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

    paths = process(INPUT_PATH, OUTPUT_DIR)

    logging.info("Result: %s" % paths)
