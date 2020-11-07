from SpaceState import SpaceState


class LOSpaceState(SpaceState):
    def __init__(self, states, links):
        super().__init__(states, links)
        self._obs_index = None
        self._has_next_obs = False

    @property
    def obs_index(self):
        return self._obs_index

    @obs_index.setter
    def obs_index(self, value):
        self._obs_index = value

    def has_next_obs(self):
        self._has_next_obs = True

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
        if not obs_list or obs_val == obs_list:
            return super()._must_add(next_out_trans)

        return False

    def is_final(self):
        if self._has_next_obs:
            return False
        return super().is_final()

    def __hash__(self):
        return hash((super().__hash__(), self._obs_index))

    def __eq__(self, obj):
        if isinstance(obj, LOSpaceState):
            if super().__eq__(obj):
                return obj.obs_index == self._obs_index

        return False

    def dict_per_json(self):
        temp = {}
        temp['name'] = self._id
        temp['obs_index'] = self._obs_index
        temp['link'] = {key: val for key, val in self._links.items()}
        temp['state'] = {
            'CFAN '+str(i): val.name for i, val in enumerate(self._states)
        }
        temp['next'] = {
            k.name: self._short_next_desc(val, k)
            for k, val in self._nexts.items()
        }

        return temp

    def _short_next_desc(self, next_state, out_trans):
        temp = {}
        temp['state'] = {
            f'CFAN {i}': st.name for i, st in enumerate(next_state.states)
        }
        temp['link'] = {name: val for name, val in next_state.links.items()}

        return temp
