class Closure:
    def __init__(self, enter_state_index, state_space):
        self._init_index = enter_state_index
        self._init_space = state_space
        self._space_state = None
        self._finals = None

    def build(self):
        self._space_state = {self._init_space[self._init_index]: None}
        temp = [self._init_space[self._init_index]]
        self._finals = {}
        for state in temp:
            has_obs = False
            for next_trans, next_state in state.nexts.items():
                if not next_trans.observable:
                    if not self._space_state.get(next_state):
                        self._space_state[next_state] = None
                        temp.append(next_state)
                else:
                    has_obs = True
            if has_obs or state.is_final():
                self._finals[state] = None
