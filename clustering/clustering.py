import numpy as np
from collections import Counter


def cluster(queries, mission_queries):
    """
    Provides cluster IDs for queries in given cluster space.

    :param queries: The queries to be given IDs.
    :param mission_queries: The queries for the mission.
    :return: `list` of cluster ids for queries.
    """
    assert isinstance(queries, np.ndarray), 'queries to be mapped must be a numpy array'
    assert len(queries.shape) == 2, 'queries must be a 2 dimensional array.'
    assert isinstance(queries, np.ndarray), 'mission_queries to be mapped must be a numpy array'
    assert len(queries.shape) == 2, 'mission_queries must be a 2 dimensional array.'

    # TODO write clustering logic.
    n_clusters = 3

    return np.random.randint(n_clusters, size=queries.shape[0])


def get_lvl_autonomy(queries, past_queries, past_feedback):
    votes = np.zeros((len(past_feedback), queries.shape[0]))

    for i, (query_preferences, past_mission_queries)in enumerate(zip(past_feedback, past_queries)):
        # Get cluster ids from mission.
        cluster_id = cluster(queries, past_mission_queries)

        # Map the cluster id to the user's preference.
        mp = np.arange(0, max(cluster_id) + 1)
        mp[past_feedback[i].keys()] = past_feedback[i].values()
        votes[i] = mp[cluster_id]

    # Find the most popular action to take from user's past feedback.
    decisions = np.zeros((queries.shape[0]))

    for i, vote in enumerate(votes.T):
        vote_counter = Counter(vote)
        decisions[i] = int(vote_counter.most_common(1)[0][0])

    return
