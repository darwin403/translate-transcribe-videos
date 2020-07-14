#! /usr/bin/python

import pymysql.cursors

import transcribe
from settings import MYSQL_DB, MYSQL_HOST, MYSQL_PASSWORD, MYSQL_USER, logging

# Connect to the database
connection = pymysql.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    db=MYSQL_DB,
    cursorclass=pymysql.cursors.DictCursor,
)

logging.info("Worker started")

with connection.cursor() as cursor:
    # find videos
    cursor.execute(
        "SELECT `id`,`videoUrl`, `status` FROM `uploadVideos` WHERE `status` in (1,3)"
    )

    videos = cursor.fetchall()

    logging.info("Pending videos: %s" % len(videos))

    # process videos
    for video in videos:

        ##############
        # NEW UPLOAD #
        ##############
        if video["status"] == 1:
            result = transcribe.process(video["videoUrl"])

            # update row
            cursor.execute(
                "UPDATE `uploadVideos` SET `status` = 2, `englishSubTitleUrl` = %s WHERE `id` = %s",
                (result["txt"], video["id"]),
            )
            connection.commit()

            logging.info("Video ID: %s status updated." % video["id"])

connection.close()

logging.info("Worker ended")
