import requests


def user_queries(participant_id):
    data = {
        "participant_id": participant_id
    }
    req = requests.post(
        "http://ec2-52-24-126-225.us-west-2.compute.amazonaws.com:81/mission/retrieve-participant-queries", data=data)
    return req.json()
