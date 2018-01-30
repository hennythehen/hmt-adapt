# Compatability Imports
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import random
import numpy as np
import requests
import sklearn.cluster as skc
from collections import Counter


def min_max_normalization(data):
    """

    Args:
        dataframe: The dataframe that contains all data to be normalized.

    Returns:
        A `Dataframe` that contains the normalized data.
        
    """

    return (data - data.min(axis=0)) / (data.max(axis=0) - data.min(axis=0))


def q_generator():
    while True:
        q_type = np.random.normal(2.5, 4, 1)
        q_conf = random.random()

        yield q_type, q_conf


def generate_fake_queries(n_queries):
    """
    Create fake queries for a mission.

    :param n_queries: The number  of queries to generate.
    :return: A `ndarray` of queries.
    """
    assert isinstance(n_queries, int), 'Number of queries must be an integer.'
    assert n_queries > 0, 'Number of queries needs to be larger than 0.'

    data = np.zeros((n_queries, 2))

    q_gen = q_generator()

    for x in range(n_queries):
        data[x] = next(q_gen)

    return data


def generate_fake_queries_sql(user_id, mission_id, n_queries):
    assert isinstance(mission_id, int), 'Mission ID must be int.'
    assert isinstance(n_queries, int), 'n_queries must be int.'

    values = []

    for x in xrange(n_queries):
        robot_id = np.random.randint(4)
        q_type = np.random.randint(4)
        operators_response = np.random.randint(4)
        true_response = np.random.randint(4)
        lvl_autonomy = np.random.randint(2)
        gcs_arrival_time = np.random.rand(1)[0] * 5

        values.append('(NULL, {}, {}, {}, {}, {}, {}, {}, {})'.format(user_id,
                                                                      robot_id,
                                                                      mission_id,
                                                                      q_type,
                                                                      operators_response,
                                                                      gcs_arrival_time,
                                                                      lvl_autonomy,
                                                                      true_response))

    return ",".join(values)


def get_mission_queries(user_id, mission_number, n_queries=100):
    # TODO Retreive queries from mission.
    return generate_fake_queries(n_queries)


def cluster(queries):
    """
    Clusters experiment queries using the DBSCAN algorithm.

    Args:
        queries: `ndarray` of mission queries to cluster.

    Returns:
        `ndarray` of cluster IDs.
    """

    normalized_queries = min_max_normalization(queries)
    return skc.DBSCAN(eps=0.11, min_samples=4).fit_predict(normalized_queries)


def predict(new_queries, mission_queries):
    mission_clusters = cluster(mission_queries)

    # Allocate space for all distances.
    distances = np.zeros((new_queries.shape[0], mission_queries.shape[0]))

    # Find distances from every new query to every mission query.
    # TODO This runs in O(n^2) time, optimize this please.
    for i, new_query in enumerate(new_queries):
        for j, mission_query in enumerate(mission_queries):
            distances[i][j] = np.linalg.norm(new_query - mission_query)

    return mission_clusters.take(np.argmin(distances, axis=1), axis=0)


def send_query_to_gcs(query):
    j = {
        "type": query["type"],
        "data": query[["query_id", "robot_id", "confidence", "file_path"]].to_json()
    }
    requests.post("http://ec2-52-24-126-225.us-west-2.compute.amazonaws.com:81/detection/send-query-to-gcs", json=j)
