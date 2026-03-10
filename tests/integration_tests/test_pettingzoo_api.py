from pettingzoo import test

import knucklebones_ml


def test_pettingzoo_api():
    env = knucklebones_ml.env()
    test.api_test(env, verbose_progress=True)
