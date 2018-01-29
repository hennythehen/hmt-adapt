from unittest import TestCase
from utils import generate_fake_queries


class TestGenerate_fake_queries(TestCase):
    def test_generate_fake_queries(self):
        import numpy as np

        mission_number = 2
        n_queries = 100
        query_features = ["confidence", "type"]

        mission_queries = generate_fake_queries(mission_number, n_queries, query_features)
        assert isinstance(mission_queries, np.ndarray), 'Output is not nd.array'
