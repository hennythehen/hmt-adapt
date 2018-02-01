import requests
import pandas as pd
import numpy as np
import sys
import utils

# Get the Participant of the mission.
req = requests.get("http://ec2-52-24-126-225.us-west-2.compute.amazonaws.com:81/iris/retrieve-last-participant")
if req.ok:
    participant_id = req.json()['data'][0]['id']
    current_mission = req.json()['data'][0]['current_mission']
    print("Query Successful")
else:
    print("Query NOT Successful")

# For now, set the mission as the first mission.
current_mission = 1
participant_id = 0
threshold = 0.8

# Retrieve query information from query
json = {
    'query_id': sys.argv[1]
}

req = requests.post("http://ec2-52-24-126-225.us-west-2.compute.amazonaws.com:81/iris/retrieve-query", json)

if req.ok:
    new_queries = pd.DataFrame(req.json()['data'])
    print("Query Successful")
else:
    print("Query NOT Successful")

json = {
    'participant_id': participant_id
}

req = requests.post("http://ec2-52-24-126-225.us-west-2.compute.amazonaws.com:81/iris/retrieve-participant-preferences",
                    json=json)

if req.ok:
    print("Query Successful")
    if current_mission < 1:
        # Error
        print("Error")
    else:
        if current_mission == 1:
            # Non Adaptive System.
            q_continue = new_queries[new_queries['confidence'] > threshold]
            q_stop = new_queries[new_queries['confidence'] < threshold]

            if len(q_stop) > 0:
                utils.send_query_to_gcs(q_stop.iloc[0])

            pass
        else:
            # Adaptive system
            data = pd.DataFrame(req.json()['data'])
            query_attributes = ["confidence", "type"]
            old_queries = data[data['mission_id'] != current_mission]
            new_queries = new_queries
            preferred_levels = data[data['mission_id'] != current_mission]['preferred_level_of_autonomy'].reset_index(
                drop=True)

            actions = -np.ones((new_queries.shape[0], 1))

            for i, query in enumerate(new_queries[query_attributes].as_matrix().astype(np.float)):
                dists = np.linalg.norm(query - old_queries[query_attributes].astype(np.float), axis=1)
                closest = np.argmin(dists)
                actions[i] = preferred_levels[closest]

            if not actions[0][0]:
                utils.send_query_to_gcs(new_queries.iloc[0])
else:
    print("Query NOT Successful")