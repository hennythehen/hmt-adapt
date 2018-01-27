from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import requests
import pandas as pd
import numpy as np
from sklearn.preprocessing import normalize
import sklearn.cluster as skc
import sys
import logging

LOG_FILENAME = "assign_cluster_ids.log"
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

user_id = sys.argv[1]

json = {
    'participant_id': 0
}
logging.info("Querying database for participant queries")
req = requests.post("http://ec2-52-24-126-225.us-west-2.compute.amazonaws.com:81/iris/retrieve-participant-queries",
                    json=json)

if req.ok:
    logging.info("Request Successful")

    data = pd.DataFrame(req.json()['data'])

    mission_queries = data[["query_id", "gcs_arrival_time", "type"]].as_matrix()

    model = skc.DBSCAN(eps=0.011, min_samples=4).fit(normalize(mission_queries[:, 1:]))

    labels = model.labels_

    cluster_assignments = np.stack((mission_queries[:, 0], labels), axis=1)

    response = dict()

    for query in cluster_assignments:
        print(query)
        response[query[0]] = query[1]

    json = {
        "cluster_assignments": response
    }

    req = requests.post("http://ec2-52-24-126-225.us-west-2.compute.amazonaws.com:81/iris/assign-cluster-ids",
                        json=json)

else:
    logging.info("Request Unsuccessful")
