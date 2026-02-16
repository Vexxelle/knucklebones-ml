from pettingzoo import AECEnv
from copy import copy

class KnucklebonesEnvironment(AECEnv):
    metadata = {
        "name": "knucklebones_environment_v0",
    }

    def __init__(self):
        self.timestep = None
        self.possible_agents = ["player_0", "player_1"]
        self.seed = None

    def reset(self, seed=None, options=None):
        self.timestep = 0
        self.agents = copy(self.possible_agents)

        if seed is not None:
            self.seed = seed

    def step(self, action):
        pass

    def render(self):
        pass

    def observation_space(self, agent):
        return self.observation_spaces[agent]

    def action_space(self, agent):
        return self.action_spaces[agent]