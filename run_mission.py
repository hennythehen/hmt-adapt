import sys
import logging
import pandas as pd

from utils.database_queries import user_queries

LOG_FILENAME = "adaptation.log"
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

user_id = sys.argv[1]
mission_id = sys.argv[2]

logging.info("==========MissionInfo==========")
logging.info(("User: " + user_id))
logging.info(("Mission : " + mission_id))

logging.debug("Querying for past user queries.")

logging.debug("Starting Mission")

running = True

while running:
    running = False

logging.info("==========MissionComplete==========\n\n")
