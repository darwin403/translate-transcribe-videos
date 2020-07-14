from dotenv import load_dotenv
import os
import logging, coloredlogs

# Configure logging
logging.basicConfig(
    filename="worker.log",
    filemode="a+",
    format="%(asctime)s,%(msecs)d [%(name)s] %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
coloredlogs.install(fmt="%(asctime)s [%(programname)s] %(levelname)s %(message)s")

# Load environment variables
load_dotenv()
load_dotenv(".env.local", override=True)

#######
# AWS #
#######

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION_NAME = os.getenv("AWS_REGION_NAME")
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")

#########
# MYSQL #
#########

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB = os.getenv("MYSQL_DB")

