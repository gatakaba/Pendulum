import numpy as np
from base_controller import BaseController


class QLearning(BaseController):
    def __init__(self):
        super().__init__()
        self.split_num = 30
        self.past_action = 0
        self.past_state = None

        # state1,state2,action
        self.Q = np.ones([self.split_num, self.split_num, self.split_num])

    def choose_action(self, state):
        index1 = self.value_to_index(state[0], 0, 2 * np.pi)
        index2 = self.value_to_index(state[1], -0.1, 0.1)

        q = self.Q[index1, index2, :]
        action_index = np.random.choice(range(self.split_num), p=np.exp(q) / np.sum(np.exp(q)))
        return self.index_to_action(action_index)

    def calc_reward(self, state):
        return 0.1 - (state[0] - np.pi) ** 2 - state[1] ** 2 * 4000

    def update_Q(self, state, past_state, past_action):
        r = self.calc_reward(state)

        index1 = self.value_to_index(state[0], 0, 2 * np.pi)
        index2 = self.value_to_index(state[1], -0.1, 0.1)

        past_index1 = self.value_to_index(past_state[0], 0, 2 * np.pi)
        past_index2 = self.value_to_index(past_state[1], -0.1, 0.1)

        past_index3 = self.value_to_index(past_action, -0.005, 0.005)

        self.Q[past_index1, past_index2, past_index3] += 0.1 * (
            r + 0.99 * np.max(self.Q[index1, index2]) - self.Q[past_index1, past_index2, past_index3])
        print(index1, index2, past_index3, r)

        return

    def value_to_index(self, value, min_value, max_value):
        x = (value - min_value) / (max_value - min_value)
        scale = np.linspace(0, 1, self.split_num)
        return np.argmin(np.abs(x - scale))

    def index_to_action(self, action_index):
        action_table = np.linspace(-0.005, 0.005, self.split_num)
        return action_table[action_index]

    def manipulate(self, state):
        if self.past_state is None:
            self.past_state = np.copy(state)
            return 0

        action = self.choose_action(state)

        self.update_Q(state, self.past_state, self.past_action)

        self.past_action = action
        self.past_state = np.copy(state)

        return action
