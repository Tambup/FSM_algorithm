from SpaceState import SpaceState


class LOSpaceState(SpaceState):
    def __init__(self, states, links):
        super().__init__(states, links)
        self._obs_index = None

    @property
    def obs_index(self):
        return self._obs_index

    @obs_index.setter
    def obs_index(self, value):
        self._obs_index = value

    def next_transition_state(self, obs_val):
        possible_next = {}
        for next_state in self._states:
            trans = [out_trans for out_trans in next_state.out_transitions
                     if self._must_add(out_trans, obs_val)]
            if trans:
                possible_next[next_state] = trans

        return possible_next

    def _must_add(self, next_out_trans, obs_val):
        obs_list = next_out_trans.observable
        if not obs_list or (obs_val in obs_list):
            return super()._must_add(next_out_trans)

        return False
